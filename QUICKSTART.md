# 🚀 Stallwache Quick Start Guide

**Deine Kamera-Konfiguration:**
```
IP: 192.168.178.108:80
RTSP-Port: 554
RTSP-URL: rtsp://192.168.178.108:554/stream
Kamera-ID: 006E07844083
DDNS: stallwache.rolleicam.net
```

---

## ⚡ 5-Minuten Setup

### 1. Test Kamera-Verbindung

```bash
python test_camera.py
```

**Erwartet:**
```
✓ PASS - network_http
✓ PASS - http_interface
✓ PASS - network_rtsp
✓ PASS - rtsp_noauth
✓ PASS - rtsp_auth
```

Wenn alle Tests grün sind → **Du bist bereit für Production!**

### 2. Konfiguration (30 Sekunden)

```bash
# Kopiere Production-Config
cp .env.production .env

# Ändere nur 2 Variablen (optional):
TELEGRAM_BOT_TOKEN=dein_token
TELEGRAM_CHAT_ID=deine_chat_id
```

Die Kamera-IP ist bereits konfiguriert ✓

### 3. Start (1 Befehl)

```bash
# Mit Docker Compose (EMPFOHLEN)
docker-compose up -d

# Logs anschauen
docker-compose logs -f stallwache
```

**Fertig! System läuft jetzt.** 🎉

---

## 📝 Detaillierte Anleitung

### Schritt 1: Voraussetzungen prüfen

```bash
# Docker installiert?
docker --version

# Python 3.10+?
python --version

# Im Stallwache-Ordner?
cd /path/to/Stallwache
ls -la config.py main.py
```

### Schritt 2: Kamera testen

```bash
# Teste mit VLC (wenn installiert)
vlc "rtsp://admin:12345@192.168.178.108:554/stream"

# Oder teste mit Python
python test_camera.py
```

### Schritt 3: Telegram einrichten (optional aber empfohlen)

Falls du Alerts bekommen möchtest:

1. **Öffne Telegram**
2. **Suche:** `@BotFather`
3. **Schreib:** `/newbot`
4. **Bot-Name:** z.B. "Stallwache Alerts"
5. **Username:** z.B. "stallwache_bot"
6. **Token kopieren:** `6012345678:ABCDEFg...`

Dann Chat-ID ermitteln:
```bash
export TOKEN="6012345678:ABCDEFg..."
curl https://api.telegram.org/bot$TOKEN/getUpdates
```

Such nach `"id": 987654321` → Das ist deine Chat-ID

### Schritt 4: .env konfigurieren

```bash
# Öffne .env.production im Editor
nano .env.production
# oder doppelklick (Windows)
```

Setze mindestens:
```env
# Kamera (bereits gesetzt)
CAMERA_RTSP_URL=rtsp://192.168.178.108:554/stream
CAMERA_USERNAME=admin
CAMERA_PASSWORD=12345

# Telegram (optional)
TELEGRAM_BOT_TOKEN=6012345678:ABCDEFg...
TELEGRAM_CHAT_ID=987654321
```

Speichern & schließen.

### Schritt 5: Mit Docker Compose starten

```bash
# Build + Start
docker-compose up -d

# Prüfe ob Container läuft
docker ps | grep stallwache

# Logs anschauen
docker-compose logs -f stallwache
```

**Erwartet in den Logs:**
```
✓ YOLOv8-Modell erfolgreich geladen
✓ RTSP-Stream-Processor initialisiert
✓ Caving-Detektor initialisiert
✓ Telegram-Client initialisiert
✓ SQLite-Datenbank initialisiert
🎬 Starte Stream-Verarbeitung...
```

### Schritt 6: Verification

```bash
# Container läuft?
docker ps -a | grep stallwache

# Logs OK?
docker logs stallwache | grep -i "error\|warning" || echo "✓ Keine Fehler"

# Datenbank exists?
ls -la data/stallwache.db

# Logs exist?
ls -la logs/
```

---

## 🧪 Live-Tests während Systemstart

### Test 1: Frame wird gelesen?

```bash
docker logs stallwache | grep -i "frame\|fps"
```

Erwartet:
```
📊 Performance | FPS: 28.5 | Frames: 300 | Alerts: 0
```

### Test 2: Telegram funktioniert?

```bash
# Manuell Alert senden:
python -c "
from telegram_client import TelegramClient
client = TelegramClient()
client.send_alert('TEST', 0.95, 0)
print('✓ Nachricht gesendet')
"
```

Dein Telegram sollte eine Nachricht bekommen ✓

### Test 3: Datenbank funktioniert?

```bash
sqlite3 data/stallwache.db "SELECT COUNT(*) FROM events;"
```

Sollte eine Zahl zurückgeben (Anzahl Events) ✓

---

## 🛑 Stoppen & Neustart

```bash
# Stoppen
docker-compose down

# Nur Container stoppen (Daten bleiben)
docker stop stallwache

# Container neustart
docker restart stallwache

# Logs anschauen (letzte 50 Zeilen)
docker logs --tail 50 stallwache

# Logs in Echtzeit
docker logs -f stallwache
```

---

## 🔥 Troubleshooting

### Problem: "Konnte RTSP-Stream nicht öffnen"

```bash
# 1. Test mit test_camera.py
python test_camera.py

# 2. Manuell testen
python -c "
import cv2
cap = cv2.VideoCapture('rtsp://admin:12345@192.168.178.108:554/stream')
print('Opened:', cap.isOpened())
cap.release()
"

# 3. Ping zur Kamera
ping 192.168.178.108

# 4. Port prüfen
nc -zv 192.168.178.108 80   # HTTP
nc -zv 192.168.178.108 554  # RTSP
```

### Problem: "Docker Container startet nicht"

```bash
# Prüfe Docker Logs
docker logs stallwache

# Prüfe .env
cat .env.production | grep CAMERA

# Prüfe Abhängigkeiten
pip list | grep opencv

# Neustart
docker-compose down
docker-compose up -d
```

### Problem: "Telegram Alerts funktionieren nicht"

```bash
# Test Bot-Token
export TOKEN="dein_token"
curl https://api.telegram.org/bot$TOKEN/getMe

# Test Message
curl https://api.telegram.org/bot$TOKEN/sendMessage \
  -d "chat_id=deine_chat_id&text=Hallo"

# Prüfe Logs auf Telegram-Fehler
docker logs stallwache | grep -i telegram
```

### Problem: "High CPU Usage"

```bash
# In .env.production:
FRAME_SKIP=2              # Überspringe Frames
RESIZE_WIDTH=640          # Kleinere Auflösung
RESIZE_HEIGHT=360
YOLO_MODEL_PATH=./models/yolov8n.pt  # Kleineres Modell (nano)
```

Dann neustart:
```bash
docker-compose down
docker-compose up -d
```

---

## 📊 Monitoring

### Live Metrics

```bash
# Prometheus Metriken
curl http://localhost:8000/metrics

# oder
watch 'curl http://localhost:8000/metrics 2>/dev/null | grep stallwache'
```

### Datenbank Abfragen

```bash
# Öffne Datenbank
sqlite3 data/stallwache.db

# Zeige letzte Events
SELECT * FROM events ORDER BY timestamp DESC LIMIT 10;

# Zähle Kalbungen
SELECT COUNT(*) FROM events WHERE event_type='CALVING_DETECTED';

# Durchschnittliche FPS
SELECT AVG(fps) FROM metrics;

# Beende sqlite
.quit
```

### Logs anschauen

```bash
# Letzte 100 Zeilen
tail -100 logs/stallwache.log

# Real-time follow
tail -f logs/stallwache.log

# Nur Fehler
grep ERROR logs/stallwache.log

# Nur Warnungen
grep WARNING logs/stallwache.log
```

---

## 🎯 Checkliste für Production

- [ ] `python test_camera.py` → ✓ ALLE TESTS PASS
- [ ] Docker installiert & läuft
- [ ] .env.production hat korrekte Werte
- [ ] Telegram Bot eingerichtet (falls gewünscht)
- [ ] `docker-compose up -d` erfolgreich
- [ ] Logs zeigen "Stream-Verarbeitung läuft"
- [ ] Telegram Alert getestet (optional)
- [ ] Datenbank funktioniert
- [ ] Metriken erreichbar (Port 8000)
- [ ] Logs speichert sich korrekt

---

## 📞 Schnelle Hilfe

**Alles grün?** → `docker-compose up -d` starten

**Problem?** → `python test_camera.py` ausführen

**Logs prüfen?** → `docker logs -f stallwache`

**Datenbank abfragen?** → `sqlite3 data/stallwache.db`

---

## 🚀 System ist bereit!

Du kannst jetzt mit folgendem Befehl starten:

```bash
docker-compose up -d
```

System läuft dann automatisch im Hintergrund.

Logs anschauen:
```bash
docker logs -f stallwache
```

Alerts kommen direkt zu Telegram! 🐄📱

---

**Viel Erfolg! Bei Fragen: stallwache123@gmail.com**
