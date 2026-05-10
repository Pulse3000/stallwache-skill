"""
RTSP Stream Processor Module
Verarbeitet Video-Streams von Netzwerk-Kameras
"""

import cv2
import numpy as np
import threading
import queue
import time
from typing import Optional
from dataclasses import dataclass

from logger import get_logger
from config import BUFFER_SIZE, STREAM_TIMEOUT, RESIZE_WIDTH, RESIZE_HEIGHT

logger = get_logger(__name__)


@dataclass
class StreamFrame:
    """Datenklasse für Stream-Frames."""
    frame: np.ndarray
    frame_number: int
    timestamp: float
    is_valid: bool = True


class RTSPStreamProcessor:
    """Verarbeitet RTSP-Streams mit Thread-Safety."""

    def __init__(
        self,
        rtsp_url: str,
        frame_skip: int = 1,
        buffer_size: int = BUFFER_SIZE,
        timeout: int = STREAM_TIMEOUT
    ):
        """
        Initialisiere Stream Processor.

        Args:
            rtsp_url: RTSP-URL der Kamera
            frame_skip: Jedes N-te Frame verarbeiten
            buffer_size: Frame-Puffer-Größe
            timeout: Verbindungs-Timeout in Sekunden
        """
        self.rtsp_url = rtsp_url
        self.frame_skip = frame_skip
        self.buffer_size = buffer_size
        self.timeout = timeout

        self.cap = None
        self.frame_queue = queue.Queue(maxsize=buffer_size)
        self.reader_thread = None
        self.is_running = False
        self.frame_count = 0
        self.skipped_frames = 0
        self.connection_errors = 0
        self.max_connection_errors = 5

        logger.info(f"RTSPStreamProcessor initialisiert | URL: {rtsp_url}")

    def start(self) -> bool:
        """Starte Stream-Verarbeitung in separatem Thread."""
        try:
            logger.info(f"Verbinde zu RTSP-Stream: {self.rtsp_url}")

            self.cap = cv2.VideoCapture(self.rtsp_url)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimale Latenz
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

            if not self.cap.isOpened():
                logger.error("Konnte RTSP-Stream nicht öffnen")
                return False

            # Stream-Properties
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(self.cap.get(cv2.CAP_PROP_FPS))

            logger.info(
                f"✓ RTSP-Verbindung hergestellt | "
                f"Resolution: {width}x{height} | FPS: {fps}"
            )

            # Starte Reader-Thread
            self.is_running = True
            self.reader_thread = threading.Thread(target=self._read_frames, daemon=True)
            self.reader_thread.start()

            return True

        except Exception as e:
            logger.error(f"Fehler beim Verbinden: {e}")
            return False

    def _read_frames(self):
        """Thread-Funktion: Lese Frames kontinuierlich aus Stream."""
        frame_number = 0

        while self.is_running:
            try:
                ret, frame = self.cap.read()

                if not ret:
                    self.connection_errors += 1
                    if self.connection_errors >= self.max_connection_errors:
                        logger.error(
                            f"Stream-Fehler {self.connection_errors} mal. Beende Reader."
                        )
                        self.is_running = False
                        break

                    logger.warning(f"Frame-Lesefehler ({self.connection_errors})")
                    time.sleep(0.1)
                    continue

                self.connection_errors = 0
                frame_number += 1

                # Frame-Skip-Logik
                if (frame_number - 1) % self.frame_skip != 0:
                    self.skipped_frames += 1
                    continue

                # Resize für schnellere Verarbeitung
                frame = cv2.resize(frame, (RESIZE_WIDTH, RESIZE_HEIGHT))

                # Frame in Queue einreihen (blockierend bei vollem Puffer)
                try:
                    self.frame_queue.put(
                        StreamFrame(
                            frame=frame,
                            frame_number=frame_number,
                            timestamp=time.time()
                        ),
                        timeout=1
                    )
                except queue.Full:
                    logger.warning("Frame-Queue voll, verwerfe ältesten Frame")
                    try:
                        self.frame_queue.get_nowait()
                        self.frame_queue.put(StreamFrame(
                            frame=frame,
                            frame_number=frame_number,
                            timestamp=time.time()
                        ), timeout=1)
                    except queue.Empty:
                        pass

            except Exception as e:
                logger.error(f"Fehler in Reader-Thread: {e}")
                time.sleep(1)

        logger.info(f"Reader-Thread beendet | Insgesamt: {frame_number} Frames")

    def read_frame(self) -> Optional[np.ndarray]:
        """
        Lese nächsten verfügbaren Frame.

        Returns:
            Frame als numpy array oder None bei Fehler
        """
        if not self.is_running and self.cap is None:
            if not self.start():
                return None

        try:
            stream_frame = self.frame_queue.get(timeout=self.timeout)
            self.frame_count += 1
            return stream_frame.frame

        except queue.Empty:
            logger.warning(f"Kein Frame verfügbar nach {self.timeout}s Timeout")
            return None

        except Exception as e:
            logger.error(f"Fehler beim Frame-Lesen: {e}")
            return None

    def get_stream_info(self) -> dict:
        """Liefere Informationen über den Stream."""
        if self.cap is None:
            return {}

        return {
            'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': int(self.cap.get(cv2.CAP_PROP_FPS)),
            'frames_read': self.frame_count,
            'frames_skipped': self.skipped_frames,
            'queue_size': self.frame_queue.qsize(),
            'connection_errors': self.connection_errors,
        }

    def release(self):
        """Gib Stream-Ressourcen frei."""
        logger.info("Gebe Stream-Ressourcen frei...")

        self.is_running = False

        if self.reader_thread:
            self.reader_thread.join(timeout=5)
            logger.info("✓ Reader-Thread beendet")

        if self.cap:
            self.cap.release()
            logger.info("✓ VideoCapture freigegeben")

        info = self.get_stream_info()
        logger.info(
            f"Stream-Statistik: "
            f"Frames: {info.get('frames_read', 0)}, "
            f"Übersprungen: {info.get('frames_skipped', 0)}, "
            f"Fehler: {info.get('connection_errors', 0)}"
        )
