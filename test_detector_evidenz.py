#!/usr/bin/env python3
"""Logiktest: Kalbung nur mit Modell-Befund (pures Python, keine Installation).

  python3 test_detector_evidenz.py

Vorher meldete der Detektor mit einem COCO-Modell jede Kuh neben einem
zweiten Objekt als Kalbung. Jetzt zaehlen nur Fruchtblase (amniotic_sac) und
Kaelberfuesse (calf_legs) mit Konfidenz > 0.80. ultralytics, cv2 und numpy
sind gestubbt.
"""
import logging
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

for name in ("cv2", "numpy", "ultralytics"):
    sys.modules[name] = types.ModuleType(name)
sys.modules["numpy"].ndarray = object
sys.modules["numpy"].mean = lambda werte: sum(werte) / len(werte)
sys.modules["ultralytics"].YOLO = object
log_stub = types.ModuleType("logger")
log_stub.get_logger = logging.getLogger
sys.modules["logger"] = log_stub

from detector import CavingDetector  # noqa: E402


class Wert:
    def __init__(self, v):
        self.v = v

    def cpu(self):
        return self

    def numpy(self):
        return self.v

    def __getitem__(self, i):
        return self.v[i]


class Box:
    def __init__(self, klasse, konf):
        self.cls = [klasse]
        self.conf = [konf]
        self.xyxy = [Wert([10.0, 20.0, 110.0, 220.0])]


class Modell:
    def __init__(self, names):
        self.names = names
        self.boxen = []

    def __call__(self, frame, **kw):
        return [types.SimpleNamespace(boxes=self.boxen, names=self.names)]


COCO = {0: "person", 19: "cow", 20: "elephant"}
EIGEN = {0: "kuh", 1: "amniotic_sac", 2: "calf_legs"}

faelle = []


def check(text, ok):
    faelle.append((text, bool(ok)))


class Sammler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.zeilen = []

    def emit(self, record):
        self.zeilen.append(record.getMessage())


sammler = Sammler()
logging.getLogger().addHandler(sammler)

# 1. COCO-Modell: zwei Kuehe + Mensch ueber viele Frames -> nie Kalbung
m = Modell(COCO)
d = CavingDetector(m, confidence_threshold=0.65)
check("1: Warnung beim Start, dass Kalbungs-Alarme aus sind",
      any("keine Geburtsklassen" in z for z in sammler.zeilen))
m.boxen = [Box(19, 0.92), Box(19, 0.88), Box(0, 0.81)]
ergebnisse = [d.detect(object()) for _ in range(10)]
check("1: zwei Kuehe + Mensch ueber 10 Frames: keine Kalbung (vorher ab Frame 7)",
      all(e and not e["calving_detected"] for e in ergebnisse))

# 2. Eigenes Modell: Fruchtblase > 0.80 -> sofort Kalbung, im ersten Frame
m = Modell(EIGEN)
sammler.zeilen.clear()
d = CavingDetector(m, confidence_threshold=0.65)
check("2: keine Warnung mit Geburtsklassen", not any("keine Geburtsklassen" in z for z in sammler.zeilen))
m.boxen = [Box(0, 0.95), Box(1, 0.84)]
e = d.detect(object())
check("2: Fruchtblase 0.84 -> Kalbung im ersten Frame", e["calving_detected"])
check("2: gemeldete Konfidenz ist die der Fruchtblase", abs(e["confidence"] - 0.84) < 1e-9)

# 3. Kaelberfuesse ebenso
m.boxen = [Box(2, 0.81)]
check("3: Kaelberfuesse 0.81 -> Kalbung", d.detect(object())["calving_detected"])

# 4. Unter der Schwelle: keine Kalbung
m.boxen = [Box(1, 0.80), Box(2, 0.79), Box(0, 0.99)]
check("4: Fruchtblase 0.80 / Fuesse 0.79 -> keine Kalbung", not d.detect(object())["calving_detected"])

# 5. Nur Kuehe im eigenen Modell: keine Kalbung
m.boxen = [Box(0, 0.99), Box(0, 0.97)]
check("5: zwei Kuehe -> keine Kalbung", not d.detect(object())["calving_detected"])

fehler = [f for f in faelle if not f[1]]
for text, ok in faelle:
    print(("OK   " if ok else "FEHL ") + text)
print(f"\nDetektor-Evidenz: {len(faelle) - len(fehler)}/{len(faelle)} Checks bestanden")
sys.exit(1 if fehler else 0)
