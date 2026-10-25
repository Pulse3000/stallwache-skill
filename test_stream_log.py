#!/usr/bin/env python3
"""Logiktest: Das Kamera-Passwort steht in keiner Logzeile des Stream-Processors.

  python3 test_stream_log.py

main.py baut die RTSP-URL mit CAMERA_USERNAME/CAMERA_PASSWORD; vorher
loggte stream_processor.py sie vollstaendig auf INFO. cv2 und numpy sind
gestubbt, es wird keine Verbindung aufgebaut.
"""
import logging
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


class ScheinCapture:
    def __init__(self, url, *a):
        self.url = url

    def set(self, *a):
        return True

    def isOpened(self):
        return False

    def get(self, *a):
        return 0


cv2 = types.ModuleType("cv2")
cv2.VideoCapture = ScheinCapture
cv2.CAP_PROP_BUFFERSIZE = cv2.CAP_PROP_AUTOFOCUS = 0
cv2.CAP_PROP_FRAME_WIDTH = cv2.CAP_PROP_FRAME_HEIGHT = cv2.CAP_PROP_FPS = 0
sys.modules["cv2"] = cv2
np = types.ModuleType("numpy")
np.ndarray = object
sys.modules["numpy"] = np
log_stub = types.ModuleType("logger")
log_stub.get_logger = logging.getLogger
sys.modules["logger"] = log_stub

import stream_processor as sp  # noqa: E402


class Sammler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.zeilen = []

    def emit(self, record):
        self.zeilen.append(record.getMessage())


sammler = Sammler()
logging.getLogger().addHandler(sammler)
logging.getLogger().setLevel(logging.DEBUG)

faelle = []


def check(text, ok):
    faelle.append((text, bool(ok)))


PASSWORT = "Kamera#Geheim-42"
URL = f"rtsp://admin:{PASSWORT.replace('#', '%23')}@192.168.178.108:554/stream"

proz = sp.RTSPStreamProcessor(rtsp_url=URL)
proz.start()  # Schein-Kamera ist nicht erreichbar -> Fehlerpfad
alles = "\n".join(sammler.zeilen)
check("1: Initialisierung und Verbindungsversuch geloggt",
      "initialisiert" in alles and "Verbinde zu RTSP-Stream" in alles)
check("1: Passwort steht in keiner Logzeile",
      PASSWORT not in alles and "Kamera%23Geheim" not in alles and "admin" not in alles)
check("1: Host und Pfad bleiben sichtbar", "rtsp://192.168.178.108:554/stream" in alles)
check("1: die Verbindung nutzt weiter die URL mit Zugangsdaten", proz.cap.url == URL)

check("2: URL ohne Zugangsdaten unveraendert",
      sp.ohne_zugangsdaten("rtsp://192.168.178.108:554/stream") == "rtsp://192.168.178.108:554/stream")
check("2: nur Benutzer wird entfernt",
      sp.ohne_zugangsdaten("rtsp://admin@cam/s1") == "rtsp://cam/s1")
check("2: IPv6 bleibt gueltig",
      sp.ohne_zugangsdaten("rtsp://u:p@[fd7a::1]:554/s") == "rtsp://[fd7a::1]:554/s")

fehler = [f for f in faelle if not f[1]]
for text, ok in faelle:
    print(("OK   " if ok else "FEHL ") + text)
print(f"\nStream-Log: {len(faelle) - len(fehler)}/{len(faelle)} Checks bestanden")
sys.exit(1 if fehler else 0)
