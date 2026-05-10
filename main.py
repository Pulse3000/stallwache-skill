#!/usr/bin/env python3
"""
Stallwache - KI-basiertes Kalberkennungs- und Stallüberwachungssystem
Main entry point für RTSP-Stream-Verarbeitung mit YOLOv8 & Telegram-Integration

Author: Stallwache Team
Version: 1.0.0
License: MIT
"""

import sys
import logging
import time
from pathlib import Path
from typing import Optional
from datetime import datetime

import cv2
import numpy as np
from ultralytics import YOLO

from config import (
    CAMERA_RTSP_URL,
    CAMERA_USERNAME,
    CAMERA_PASSWORD,
    YOLO_MODEL_PATH,
    CONFIDENCE_THRESHOLD,
    FRAME_SKIP,
    LOG_LEVEL,
    ENABLE_TELEGRAM,
    ENABLE_DATABASE,
    DEBUG_MODE,
)
from logger import setup_logging, get_logger
from database import Database
from telegram_client import TelegramClient
from stream_processor import RTSPStreamProcessor
from detector import CavingDetector
from metrics import MetricsCollector

logger = get_logger(__name__)


class StallwacheSystem:
    """Hauptsystem für Kalberkennungs- und Stallüberwachung."""

    def __init__(self):
        """Initialisiere Stallwache-System."""
        self.rtsp_url = self._build_rtsp_url()
        self.yolo_model = None
        self.detector = None
        self.stream_processor = None
        self.telegram_client = None
        self.database = None
        self.metrics = None
        self.is_running = False
        self.frame_count = 0

        logger.info("="*60)
        logger.info("🐄 Stallwache System Initialisierung")
        logger.info("="*60)

    def _build_rtsp_url(self) -> str:
        """Konstruiere RTSP-URL mit Authentifizierung."""
        if CAMERA_USERNAME and CAMERA_PASSWORD:
            return CAMERA_RTSP_URL.replace(
                "rtsp://", f"rtsp://{CAMERA_USERNAME}:{CAMERA_PASSWORD}@"
            )
        return CAMERA_RTSP_URL

    def initialize(self) -> bool:
        """Initialisiere alle Komponenten des Systems."""
        try:
            logger.info("Starte Komponenten-Initialisierung...")

            # 1. YOLOv8 Modell laden
            logger.info(f"📦 Lade YOLOv8-Modell: {YOLO_MODEL_PATH}")
            self.yolo_model = YOLO(YOLO_MODEL_PATH)
            logger.info("✓ YOLOv8-Modell erfolgreich geladen")

            # 2. Detektor initialisieren
            self.detector = CavingDetector(
                model=self.yolo_model,
                confidence_threshold=CONFIDENCE_THRESHOLD,
                debug_mode=DEBUG_MODE
            )
            logger.info("✓ Caving-Detektor initialisiert")

            # 3. Stream-Processor initialisieren
            self.stream_processor = RTSPStreamProcessor(
                rtsp_url=self.rtsp_url,
                frame_skip=FRAME_SKIP
            )
            logger.info("✓ RTSP-Stream-Processor initialisiert")

            # 4. Telegram-Client initialisieren (optional)
            if ENABLE_TELEGRAM:
                self.telegram_client = TelegramClient()
                if not self.telegram_client.test_connection():
                    logger.warning("⚠️  Telegram-Verbindung konnte nicht getestet werden")
                else:
                    logger.info("✓ Telegram-Client initialisiert")

            # 5. Datenbank initialisieren (optional)
            if ENABLE_DATABASE:
                self.database = Database()
                self.database.initialize()
                logger.info("✓ SQLite-Datenbank initialisiert")

            # 6. Metrics-Collector initialisieren
            self.metrics = MetricsCollector()
            logger.info("✓ Metrics-Collector initialisiert")

            logger.info("="*60)
            logger.info("✓ Alle Komponenten erfolgreich initialisiert!")
            logger.info("="*60)
            return True

        except Exception as e:
            logger.error(f"❌ Fehler bei System-Initialisierung: {e}", exc_info=True)
            return False

    def run(self):
        """Starte Hauptschleife der Stream-Verarbeitung."""
        if not self.initialize():
            logger.error("System-Initialisierung fehlgeschlagen. Beende.")
            return

        self.is_running = True
        consecutive_errors = 0
        max_consecutive_errors = 5

        logger.info("🎬 Starte Stream-Verarbeitung...")

        try:
            while self.is_running:
                try:
                    # Frame aus Stream lesen
                    frame = self.stream_processor.read_frame()

                    if frame is None:
                        consecutive_errors += 1
                        if consecutive_errors >= max_consecutive_errors:
                            logger.error("Zu viele Stream-Fehler. Beende.")
                            break
                        logger.warning(f"Frame-Lesefehler ({consecutive_errors}/{max_consecutive_errors})")
                        time.sleep(1)
                        continue

                    consecutive_errors = 0
                    self.frame_count += 1

                    # Kalberkennungs-Inferenz
                    results = self.detector.detect(frame)

                    # Metriken aktualisieren
                    self.metrics.update_frame_count(self.frame_count)

                    # Bei Erkennung: Alert + Logging
                    if results and results['calving_detected']:
                        confidence = results['confidence']
                        logger.warning(
                            f"🚨 KALBUNG ERKANNT! "
                            f"Confidence: {confidence:.2%} | "
                            f"Frame: {self.frame_count}"
                        )

                        # Speichere Event in Datenbank
                        if self.database:
                            self.database.log_event(
                                event_type="CALVING_DETECTED",
                                confidence=confidence,
                                frame_number=self.frame_count,
                                timestamp=datetime.now()
                            )

                        # Sende Telegram-Alert
                        if self.telegram_client:
                            self.telegram_client.send_alert(
                                event_type="CALVING",
                                confidence=confidence,
                                frame_number=self.frame_count,
                                frame_image=frame
                            )

                        self.metrics.increment_alerts()

                    # Performance-Metriken
                    if self.frame_count % 300 == 0:  # Alle ~10 Sekunden (30fps)
                        fps = self.metrics.get_fps()
                        alerts = self.metrics.get_alert_count()
                        logger.info(
                            f"📊 Performance | FPS: {fps:.1f} | "
                            f"Frames: {self.frame_count} | Alerts: {alerts}"
                        )

                        if self.database:
                            self.database.log_metrics(fps=fps)

                except KeyboardInterrupt:
                    logger.info("⏹️  Stream-Verarbeitung durch Benutzer unterbrochen")
                    break

                except Exception as e:
                    logger.error(f"Fehler in Hauptschleife: {e}", exc_info=True)
                    time.sleep(1)

        finally:
            self.cleanup()

    def cleanup(self):
        """Räume auf und schließe Ressourcen."""
        logger.info("🧹 Räume Ressourcen auf...")
        self.is_running = False

        if self.stream_processor:
            self.stream_processor.release()
            logger.info("✓ Stream-Processor freigegeben")

        if self.database:
            self.database.close()
            logger.info("✓ Datenbank geschlossen")

        logger.info("="*60)
        logger.info(f"Session beendet | Gesamt-Frames: {self.frame_count}")
        logger.info("="*60)


def main():
    """Haupteinstiegspunkt."""
    setup_logging(level=LOG_LEVEL)

    system = StallwacheSystem()

    try:
        system.run()
    except KeyboardInterrupt:
        logger.info("Beende durch Benutzer...")
    except Exception as e:
        logger.critical(f"Kritischer Fehler: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
