# CLAUDE.md — stallwache-skill

Älterer, eigenständiger Prototyp: IP-Kamera (RTSP) → YOLOv8 → Telegram, mit
SQLite-Protokoll und einer kleinen Vercel-API. Verpackt als Skill-Paket
`stallwache-skill.skill`.

**Das gepflegte System liegt im Repo `Pulse3000/Die_Stallwache`** (Webapp +
Edge-Agent, Erkennungsregeln, Roadmap, Arbeitsvorrat). Neue Funktionen und
Regeln gehören dorthin. Hier wird nur gehalten und korrigiert.

## Stand — ohne Beschönigung

- **Mit dem Standardmodell gibt es keinen Kalbungs-Alarm.** `detector.py`
  meldet eine Kalbung nur bei Modell-Befund: Klasse `amniotic_sac` oder
  `calf_legs`, Konfidenz über 0.80. `yolov8m.pt` (COCO) kennt diese Klassen
  nicht; der Detektor warnt beim Start und schweigt. Das ist Absicht.
- **Es gibt kein trainiertes Modell** in diesem Repo.
- **Leistungszahlen** in `SKILL.md`, `README.md` und den Launch-Dokumenten
  (FPS, Latenz, Verfügbarkeit) sind Zielwerte, nicht gemessen.
- **`api_handler.py` ist tot:** Es importiert Namen, die es nicht gibt
  (`Config`, `YOLODetector`, `RTSPProcessor`). Der Vercel-Weg ist
  `api/handler.py` → `vercel_app.py`.
- **Altes Kamera-Passwort in der Git-Historie.** Aus Code, Doku und Paket ist
  es entfernt; ungültig wird es nur, wenn der Betreiber es an der Kamera
  ändert.

## Regeln

1. **Kalbung nur mit Modell-Befund.** „Kuh plus zweites Objekt" ist kein
   Geburtsbefund. `test_detector_evidenz.py` hält das fest — diesen Test nie
   abschwächen.
2. **Keine Zugangsdaten** in Code, Doku, Beispielen oder Logzeilen.
   `test_stream_log.py` prüft das Log.
3. **Paket = Repo.** Jede Datei im Paket ist byte-gleich mit dem Repo. Nach
   jeder Änderung an einer Paketdatei (`PAKET_DATEIEN` in `paket_bauen.py`):
   `python3 paket_bauen.py` und das Paket mit committen.
4. **Schwellen ändert nur der Betreiber.** Bekannter Unterschied zum
   Edge-Agenten: hier `> 0.80`, dort `>= 0.80`. Nicht eigenmächtig angleichen.
5. **Keine unbelegten Zahlen** neu in die Doku schreiben. Was nicht am Gerät
   gemessen ist, heißt „Zielwert" oder steht nicht da.
6. **`archiv/` ist nicht maßgeblich.** Dort liegen überholte Status-,
   Launch- und Einrichtungsdokumente. Nicht daraus zitieren, nicht pflegen.

## Befehle

```bash
bash pruefen.sh                    # alles: Syntax, beide Logiktests, Paket == Repo
python3 test_detector_evidenz.py   # Kalbung nur mit Modell-Befund
python3 test_stream_log.py         # kein Passwort im Log
python3 paket_bauen.py             # Paket neu bauen (und prüfen)
python3 paket_bauen.py --pruefen   # nur prüfen
```

Die Tests sind pures Python; `cv2`, `numpy`, `ultralytics` werden gestubbt.
**Nichts installieren.** `test_camera.py`, `test_vercel_api.py` und
`probe_stream.py` brauchen eine Kamera bzw. installierte Pakete und laufen
nicht in einer Cloud-Sitzung.

## Karte

| Ort | Inhalt |
| --- | --- |
| `main.py` | Hauptschleife: Stream lesen, erkennen, melden |
| `detector.py` | `CavingDetector` — die Regel „Kalbung nur mit Modell-Befund" |
| `stream_processor.py` | RTSP-Verbindung, schwärzt Zugangsdaten im Log |
| `telegram_client.py`, `database.py`, `metrics.py`, `logger.py`, `config.py` | Versand, SQLite, Kennzahlen, Log, Konfiguration aus Umgebungsvariablen |
| `vercel_app.py`, `api/handler.py`, `vercel.json` | Vercel-API |
| `SKILL.md`, `evals.json`, `marketplace-metadata.json` | Skill-Beschreibung und Marktplatz-Angaben |
| `stallwache-skill.skill` | das veröffentlichte Paket (ZIP), gebaut von `paket_bauen.py` |
| `docs/` | Hardware-Einrichtung der Rollei HD 20 |
| `archiv/` | überholte Dokumente und Einmal-Skripte, nicht maßgeblich |

## Arbeitsablauf

1. Änderung klein halten, `bash pruefen.sh` grün.
2. PR als Entwurf. **Kein Agent mergt in diesem Repo selbst** — hier gibt es
   keine Merge-Freigabe des Betreibers.
3. Fragen statt handeln bei: Schwellen, Paketinhalt, Marktplatz-Angaben,
   allem, was Geld kostet oder Zugangsdaten braucht.

## Offene Punkte für den Betreiber

- Kamera-Passwort an der Kamera ändern (steht in der Git-Historie).
- Entscheiden, ob dieses Repo weitergeführt oder stillgelegt wird, seit der
  Edge-Agent in `Die_Stallwache` die Erkennung trägt.
- `GitHub_README.md`, `DEPLOY_NOW.md` und `VERCEL_DEPLOYMENT_COMPLETE.md`
  sind Teil des Pakets und nennen ungemessene Zahlen — überarbeiten oder aus
  dem Paket nehmen.
