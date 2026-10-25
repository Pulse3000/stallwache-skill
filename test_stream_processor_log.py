#!/usr/bin/env python3
"""Logiktest: RTSP-Zugangsdaten landen nie im Log (pures Python, keine Installation).

  python3 test_stream_processor_log.py

Vorher schrieb der Stream-Processor die von main.py gebaute URL
rtsp://USER:PASSWORT@host/... zweimal im Klartext ins INFO-Log. Jetzt wird
user:pass@ vor dem Loggen entfernt; cv2 bekommt weiter die volle URL.
cv2, numpy und die schweren Module von main.py sind gestubbt.
"""
import logging
import os
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

BENUTZER = "stallnutzer"
PASSWORT = "Test-Pw-7xQ2"
os.environ["CAMERA_RTSP_URL"] = "rtsp://192.168.178.108:554/stream"
os.environ["CAMERA_USERNAME"] = BENUTZER
os.environ["CAMERA_PASSWORD"] = PASSWORT

for name in ("cv2", "numpy", "ultralytics", "database", "telegram_client", "detector", "metrics"):
    sys.modules[name] = types.ModuleType(name)
sys.modules["numpy"].ndarray = object
sys.modules["ultralytics"].YOLO = object
sys.modules["database"].Database = object
sys.modules["telegram_client"].TelegramClient = object
sys.modules["detector"].CavingDetector = object
sys.modules["metrics"].MetricsCollector = object
log_stub = types.ModuleType("logger")
log_stub.get_logger = logging.getLogger
log_stub.setup_logging = lambda *a, **kw: logging.getLogger()
sys.modules["logger"] = log_stub

cv2 = sys.modules["cv2"]
for i, konstante in enumerate(("CAP_PROP_BUFFERSIZE", "CAP_PROP_AUTOFOCUS", "CAP_PROP_FRAME_WIDTH",
                               "CAP_PROP_FRAME_HEIGHT", "CAP_PROP_FPS")):
    setattr(cv2, konstante, i)


class Kamera:
    """VideoCapture-Ersatz: merkt sich die URL, liefert nie ein Frame."""
    geoeffnet = []

    def __init__(self, url):
        Kamera.geoeffnet.append(url)

    def set(self, *a):
        return True

    def get(self, prop):
        return 0

    def isOpened(self):
        return True

    def read(self):
        return False, None

    def release(self):
        pass


cv2.VideoCapture = Kamera
cv2.resize = lambda frame, groesse: frame

import main  # noqa: E402
from stream_processor import RTSPStreamProcessor, url_ohne_zugangsdaten  # noqa: E402

faelle = []


def check(text, ok):
    faelle.append((text, bool(ok)))


class Sammler(logging.Handler):
    def __init__(self):
        super().__init__(level=logging.DEBUG)
        self.zeilen = []

    def emit(self, record):
        self.zeilen.append(self.format(record))


sammler = Sammler()
logging.getLogger().addHandler(sammler)
logging.getLogger().setLevel(logging.DEBUG)

# 1. URL wie in main.py gebaut -> Processor anlegen, starten, freigeben
url = main.StallwacheSystem._build_rtsp_url(None)
check("1: main.py baut die URL mit Zugangsdaten (Testvoraussetzung)", f"{BENUTZER}:{PASSWORT}@" in url)
p = RTSPStreamProcessor(url, timeout=1)
check("1: start() gelingt mit Kamera-Stub", p.start())
p.reader_thread.join(timeout=5)
p.release()
check("1: Log-Zeilen wurden erfasst (sonst waere der Test wertlos)",
      any("initialisiert" in z for z in sammler.zeilen) and any("Verbinde zu" in z for z in sammler.zeilen))
check("1: Passwort steht in keiner Log-Zeile", not any(PASSWORT in z for z in sammler.zeilen))
check("1: Benutzername steht in keiner Log-Zeile", not any(BENUTZER in z for z in sammler.zeilen))
check("1: Log nennt weiter Host, Port und Pfad",
      any("rtsp://192.168.178.108:554/stream" in z for z in sammler.zeilen))
check("1: cv2 bekommt die volle URL mit Zugangsdaten", Kamera.geoeffnet == [url])

# 2. Unkodiertes / ? # @ im Passwort: urlsplit endet den Host-Teil zu frueh
for zeichen in "/?#@":
    pw = f"ab{zeichen}cd-9"
    sauber = url_ohne_zugangsdaten(f"rtsp://admin:{pw}@10.0.0.5:554/live")
    check(f"2: Passwort mit '{zeichen}' -> nichts davon im Log ({sauber})",
          "cd-9" not in sauber and "admin" not in sauber and sauber == "rtsp://10.0.0.5:554/live")

# 3. Ohne Zugangsdaten bleibt die URL unveraendert
for roh in ("rtsp://192.168.178.108:554/stream", "rtsp://[fe80::1]:554/h264?kanal=1"):
    check(f"3: {roh} unveraendert", url_ohne_zugangsdaten(roh) == roh)

# 4. Kaputte URL: kein Absturz, kein Klartext
check("4: ungueltige IPv6-URL -> Platzhalter statt Exception",
      url_ohne_zugangsdaten(f"rtsp://admin:{PASSWORT}@[fe80::1/stream") == "<ungültige URL>")

fehler = [f for f in faelle if not f[1]]
for text, ok in faelle:
    print(("OK   " if ok else "FEHL ") + text)
print(f"\nStream-Log ohne Zugangsdaten: {len(faelle) - len(fehler)}/{len(faelle)} Checks bestanden")
sys.exit(1 if fehler else 0)
