#!/usr/bin/env python3
"""Baut und prueft das Skill-Paket stallwache-skill.skill.

    python3 paket_bauen.py            # Paket aus dem Repo-Stand neu bauen
    python3 paket_bauen.py --pruefen  # nur pruefen: Paket == Repo-Stand?

Regel: Jede Datei im Paket ist byte-gleich mit der Datei im Repo. Das
veroeffentlichte Paket vom Mai 2026 trug noch ein Kamera-Passwort und einen
Detektor, der jede Kuh neben einem zweiten Objekt als Kalbung meldete –
weil es nach den Korrekturen im Repo nicht neu gebaut wurde. Diese Pruefung
macht so einen Rueckstand rot, statt darauf zu hoffen, dass ihn jemand
bemerkt.

Nach jeder Aenderung an einer Datei aus PAKET_DATEIEN: neu bauen und das
Paket mit committen. Pures Python, keine Abhaengigkeiten.
"""

import sys
import zipfile
from pathlib import Path

HIER = Path(__file__).resolve().parent
PAKET = HIER / "stallwache-skill.skill"

# Inhalt und Reihenfolge des Pakets. Eine Datei aufnehmen oder entfernen ist
# eine Entscheidung ueber das veroeffentlichte Produkt – nicht nebenbei aendern.
PAKET_DATEIEN = [
    ".env.example",
    "CHANGELOG.md",
    "config.py",
    "CONTRIBUTING.md",
    "database.py",
    "DEPLOY_NOW.md",
    "detector.py",
    "docker-compose.yml",
    "Dockerfile",
    "GitHub_README.md",
    "LICENSE",
    "logger.py",
    "main.py",
    "metrics.py",
    "QUICKSTART.md",
    "requirements.txt",
    "SKILL.md",
    "stream_processor.py",
    "telegram_client.py",
    "test_vercel_api.py",
    "vercel_app.py",
    "VERCEL_DEPLOYMENT_COMPLETE.md",
    "VERCEL_QUICK_START.md",
    "vercel.json",
]

# Fester Zeitstempel: Zwei Laeufe aus demselben Stand ergeben dasselbe Archiv,
# ein Neubau ohne inhaltliche Aenderung erzeugt keinen Git-Unterschied.
FESTE_ZEIT = (2026, 1, 1, 0, 0, 0)


def bauen() -> None:
    fehlend = [name for name in PAKET_DATEIEN if not (HIER / name).is_file()]
    if fehlend:
        sys.exit(f"Paket nicht gebaut – Dateien fehlen: {', '.join(fehlend)}")
    with zipfile.ZipFile(PAKET, "w", zipfile.ZIP_DEFLATED) as archiv:
        for name in PAKET_DATEIEN:
            info = zipfile.ZipInfo(name, date_time=FESTE_ZEIT)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archiv.writestr(info, (HIER / name).read_bytes())
    print(f"Paket gebaut: {PAKET.name} ({len(PAKET_DATEIEN)} Dateien)")


def pruefen() -> int:
    """Gibt die Zahl der Befunde zurueck (0 = Paket entspricht dem Repo)."""
    if not PAKET.is_file():
        print(f"FEHL {PAKET.name} fehlt")
        return 1
    befunde = 0
    with zipfile.ZipFile(PAKET) as archiv:
        defekt = archiv.testzip()
        if defekt:
            print(f"FEHL Archiv beschaedigt bei {defekt}")
            befunde += 1
        im_paket = archiv.namelist()
        if im_paket != PAKET_DATEIEN:
            zuviel = sorted(set(im_paket) - set(PAKET_DATEIEN))
            zuwenig = sorted(set(PAKET_DATEIEN) - set(im_paket))
            print(
                "FEHL Dateiliste weicht ab"
                + (f" | nur im Paket: {zuviel}" if zuviel else "")
                + (f" | fehlt im Paket: {zuwenig}" if zuwenig else "")
                + ("" if zuviel or zuwenig else " | Reihenfolge anders")
            )
            befunde += 1
        for name in im_paket:
            datei = HIER / name
            if not datei.is_file():
                continue  # schon als Listenabweichung gemeldet
            if archiv.read(name) != datei.read_bytes():
                print(f"FEHL {name}: Paket und Repo unterscheiden sich")
                befunde += 1
    if befunde == 0:
        print(f"OK   Paket entspricht dem Repo-Stand ({len(im_paket)} Dateien)")
    else:
        print("\nAbhilfe: python3 paket_bauen.py  (und das Paket mit committen)")
    return befunde


if __name__ == "__main__":
    if "--pruefen" in sys.argv[1:]:
        sys.exit(1 if pruefen() else 0)
    bauen()
    sys.exit(1 if pruefen() else 0)
