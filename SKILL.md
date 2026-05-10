---
name: stallwache-deployment
description: "Deploy a production-ready AI-powered calf birthing detection and cattle monitoring system. Use this skill whenever a user wants to: set up real-time cattle monitoring with AI detection (YOLOv8), deploy a calf birthing alert system with Telegram notifications, configure RTSP camera streams for livestock surveillance, set up 24/7 automated monitoring with Docker, or integrate hardware monitoring systems for farms. This skill handles the complete deployment pipeline from hardware setup through production deployment with Docker, database configuration, logging, monitoring metrics, and full system documentation."
compatibility: "Docker, docker-compose, Python 3.10+, Telegram Bot API (optional for alerts)"
---

# Stallwache - AI-basiertes Kalberkennungs-Überwachungssystem

## 🎯 Überblick

Stallwache ist ein **produktionsreifes, vollautomatisiertes System** zur Erkennung von Kalbungen in Rinderbeständen mittels künstlicher Intelligenz. Das System verarbeitet in Echtzeit Video-Streams von Stallkameras (RTSP), analysiert diese mit YOLOv8-KI-Modellen und sendet automatisch Benachrichtigungen per Telegram an den Landwirt.

### Was macht Stallwache?

1. **Video-Stream-Verarbeitung**: Liest RTSP-Streams von IP-Kameras in Echtzeit (30 FPS @ 1080p)
2. **KI-Detektion**: Erkennt Kühe und Kälber mittels YOLOv8-Modellen
3. **Kalberungs-Analyse**: Temporale Analyse über mehrere Frames hinweg für genaue Erkennung
4. **Alerts**: Sendet Telegram-Nachrichten mit Bildern an den Landwirt
5. **Datenbank-Logging**: Speichert alle Events in SQLite-Datenbank
6. **Performance-Monitoring**: Überwacht FPS, Inferenz-Zeit und System-Uptime
7. **Produktions-Readiness**: Docker-Container, Health-Checks, Error-Handling, Logging

### Erwartete Performance

- **Verarbeitung**: 28-30 FPS @ 1080p
- **CPU-Auslastung**: 30-60% (Single Core)
- **RAM**: 2-3 GB
- **Latenz bis Alert**: ~2 Sekunden
- **Uptime**: 24/7 durch Docker Restart Policy

---

## 📋 Anforderungen vor dem Start

### Hardware
- **Kamera**: IP-Kamera mit RTSP-Stream-Unterstützung (z.B. Rollei Safetycam HD 20)
- **Compute**: Standard-PC/Laptop oder Raspberry Pi 4+
- **Netzwerk**: Stabile Verbindung zur Kamera

### Software
- **Docker & Docker-Compose** installiert
- **Python 3.10+** (für Pre-Deployment-Tests)
- **Git** (für Versionskontrolle)
- **Telegram Bot Token** (optional, für Alerts)

### Konfiguration erforderlich
- Kamera-IP-Adresse
- RTSP-Stream-URL
- Kamera-Username & Password
- (Optional) Telegram Bot Token und Chat-ID

---

## 🚀 Schritt-für-Schritt Deployment

### Phase 1: Vorbereitung (5 Minuten)

#### 1.1 Kamera-Informationen sammeln

```bash
# Notiere diese Informationen:
- Kamera IP-Adresse: (z.B. 192.168.178.108:80)
- RTSP URL: (z.B. rtsp://192.168.178.108:554/stream)
- Username: (Standard oder konfiguriert)
- Password: (Standard oder konfiguriert)
```

#### 1.2 Telegram Bot einrichten (optional aber empfohlen)

```bash
1. Öffne Telegram → Suche @BotFather
2. Schreib /newbot
3. Bot-Name: z.B. "Stallwache Alerts"
4. Bot-Username: z.B. "stallwache_bot"
5. NOTIERE den Token: 6012345678:ABCDEFg...

6. Schreib eine Nachricht an deinen neuen Bot
7. Terminal:
   export TOKEN="dein_token_hier"
   curl https://api.telegram.org/bot$TOKEN/getUpdates
8. NOTIERE die Chat-ID aus der Antwort
```

### Phase 2: System Setup (10 Minuten)

#### 2.1 Projekt-Verzeichnis erstellen

```bash
mkdir -p ~/stallwache && cd ~/stallwache
```

#### 2.2 Konfigurationsdateien erstellen

Erstelle `.env.production` mit deinen Werten:

```env
# CAMERA CONFIGURATION
CAMERA_RTSP_URL=rtsp://192.168.178.108:554/stream
CAMERA_USERNAME=dein_username
CAMERA_PASSWORD=dein_password

# AI MODEL CONFIGURATION
YOLO_MODEL_PATH=./models/yolov8m.pt
CONFIDENCE_THRESHOLD=0.65
IOU_THRESHOLD=0.45

# TELEGRAM CONFIGURATION
ENABLE_TELEGRAM=true
TELEGRAM_BOT_TOKEN=6012345678:ABCDEFg...
TELEGRAM_CHAT_ID=987654321
TELEGRAM_SEND_IMAGE=true
TELEGRAM_ALERT_COOLDOWN=60

# DATABASE CONFIGURATION
ENABLE_DATABASE=true
DATABASE_PATH=./data/stallwache.db
LOG_RETENTION_DAYS=30

# LOGGING CONFIGURATION
LOG_LEVEL=INFO
LOG_DIR=./logs
LOG_MAX_SIZE=10485760
LOG_BACKUP_COUNT=5

# SYSTEM CONFIGURATION
DEBUG_MODE=false
DEVICE=cpu
NUM_WORKERS=4
STREAM_TIMEOUT=30
INFERENCE_TIMEOUT=5

# FEATURE FLAGS
FEATURE_MULTI_CAMERA=false
FEATURE_CLOUD_BACKUP=false
FEATURE_WEB_DASHBOARD=false
```

### Phase 3: Validierung (5 Minuten)

#### 3.1 Kamera-Verbindung testen

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
✓ ALLE TESTS BESTANDEN (5/5)
🚀 System ist bereit für Production-Start!
```

Falls FAIL → siehe Troubleshooting-Sektion

### Phase 4: Deployment (2 Minuten)

#### 4.1 System starten

```bash
docker-compose up -d
```

#### 4.2 Container-Status prüfen

```bash
docker ps | grep stallwache
# Sollte zeigen: stallwache ... Up 5 seconds
```

#### 4.3 Logs überwachen

```bash
docker logs -f stallwache
```

**Erwartet:**
```
✓ YOLOv8-Modell erfolgreich geladen
✓ RTSP-Stream-Processor initialisiert
✓ SQLite-Datenbank initialisiert
✓ Telegram-Client initialisiert
🎬 Starte Stream-Verarbeitung...
📊 Performance | FPS: 28.5 | Frames: 300 | Alerts: 0
```

### Phase 5: Verifikation (5 Minuten)

#### 5.1 Health Check ausführen

```bash
bash health_check.sh
```

**Erwartet:**
```
✓ Container läuft
✓ Kamera erreichbar
✓ Metriken OK
✓ Datenbank OK
```

#### 5.2 Erste Detektionen prüfen

```bash
# Datenbank-Abfrage
sqlite3 data/stallwache.db "SELECT * FROM events LIMIT 5;"

# Oder: Zeige ein Kuh-Video vor die Kamera
# System sollte Events loggen und (falls Telegram aktiv) Alerts senden
```

---

## 📊 System-Architektur

### Komponenten-Übersicht

```
┌─────────────────────────────────────────────────────┐
│         RTSP-Stream (Rollei Kamera)                │
│       192.168.178.108:554/stream                   │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│         stream_processor.py                          │
│  • RTSP-Frame-Dekodierung                          │
│  • Thread-Safe Queue                               │
│  • Auto-Reconnect bei Fehlern                      │
│  • Frame-Buffering & Latenz-Optimierung            │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│         detector.py (YOLOv8)                        │
│  • Objekt-Detektion                                │
│  • Kalberungs-Logik                                │
│  • Temporal Analysis (Frame-Konsistenz)            │
│  • Confidence Filtering                            │
└──────────────────┬──────────────────────────────────┘
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
  ┌──────────────┐  ┌──────────────────┐
  │ telegram_    │  │   database.py    │
  │ client.py    │  │  • Events loggen │
  │  • Alerts    │  │  • Metriken      │
  │  • Bilder    │  │  • Auto-Cleanup  │
  └──────────────┘  └──────────────────┘
```

### Python-Module (Gesamtumfang: ~1.160 Zeilen)

#### 1. main.py (180 Zeilen)
- Haupteinstiegspunkt
- Orchestriert alle Komponenten
- Handling von Signals (Graceful Shutdown)
- Error Recovery

#### 2. config.py (130 Zeilen)
- Zentrale Konfiguration
- 30+ Environment-Variablen
- Validierung beim Start

#### 3. stream_processor.py (160 Zeilen)
- RTSP-Stream-Verarbeitung
- Thread-Safe Frame Queue
- Auto-Reconnect
- Latenz-Optimierung

#### 4. detector.py (190 Zeilen)
- YOLOv8 Inferenz
- Kalberungs-Erkennungslogik
- Temporal Analysis
- Debug-Visualisierung

#### 5. telegram_client.py (140 Zeilen)
- Telegram Bot Integration
- Alert-Versand mit Bildern
- Cooldown-Management
- Error Handling

#### 6. database.py (210 Zeilen)
- SQLite Datenbank
- Event-Logging
- Detektions-Protokollierung
- Metriken-Speicherung
- Auto-Cleanup

#### 7. logger.py (80 Zeilen)
- Logging mit Rotating Files
- Farbige Console-Ausgabe
- Error & Main Log Separation

#### 8. metrics.py (70 Zeilen)
- Performance Monitoring
- FPS-Tracking
- Inferenz-Zeit Messung
- Uptime Calculation

---

## 🔧 Häufige Befehle

```bash
# Logs live anschauen
docker logs -f stallwache

# Letzte 100 Log-Zeilen
docker logs --tail 100 stallwache

# System stoppen
docker-compose down

# System neu starten
docker-compose restart stallwache

# Health Check
bash health_check.sh

# Datenbank-Abfrage
sqlite3 data/stallwache.db "SELECT COUNT(*) FROM events;"

# Performance-Metriken
curl http://localhost:8000/metrics

# Docker-Stats anschauen
docker stats stallwache

# Backup erstellen
cp data/stallwache.db data/stallwache.db.backup
```

---

## 🆘 Troubleshooting

### Problem: test_camera.py schlägt fehl

**Symptom**: `✗ FAIL - network_http` oder andere Test-Fehler

**Lösungen**:
```bash
# 1. Ping zur Kamera
ping 192.168.178.108

# 2. Mit VLC testen
vlc "rtsp://username:password@192.168.178.108:554/stream"

# 3. Konfiguration prüfen
cat .env.production | grep CAMERA

# 4. RTSP-Port prüfen
nmap -p 554 192.168.178.108
```

### Problem: Container startet nicht

**Symptom**: `docker ps` zeigt keinen stallwache-Container

**Lösungen**:
```bash
# Logs prüfen
docker logs stallwache

# Container neu bauen
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# Docker-Daemon prüfen
docker version

# Volumes prüfen
docker volume ls
```

### Problem: Kein Video-Stream geladen

**Symptom**: Logs zeigen "Frame queue empty" oder "Connection timeout"

**Lösungen**:
```bash
# Credentials in .env prüfen
grep CAMERA .env.production

# RTSP-URL validieren
ffprobe rtsp://user:pass@192.168.178.108:554/stream

# Firewall prüfen
sudo ufw allow 554
```

### Problem: Telegram-Alerts funktionieren nicht

**Symptom**: Bot sendet keine Nachrichten

**Lösungen**:
```bash
# Bot-Token validieren
TOKEN="dein_token"
curl https://api.telegram.org/bot$TOKEN/getMe

# Test-Nachricht senden
CHAT_ID="deine_chat_id"
curl https://api.telegram.org/bot$TOKEN/sendMessage \
  -d "chat_id=$CHAT_ID&text=Test"

# Telegram-Logs prüfen
docker logs stallwache | grep -i telegram
```

### Problem: Hohe CPU-Auslastung

**Symptom**: System nutzt >80% CPU

**Lösungen**:
```bash
# FRAME_SKIP erhöhen (weniger Frames verarbeiten)
# In .env.production:
FRAME_SKIP=2  # Nur jedes 2. Frame
FRAME_SKIP=3  # Nur jedes 3. Frame

# Modell verkleinern
YOLO_MODEL_PATH=./models/yolov8s.pt  # Small statt Medium

# Resolution reduzieren
RESIZE_WIDTH=640
RESIZE_HEIGHT=480

# System neu starten
docker-compose down
docker-compose up -d
```

---

## ✅ Checkliste nach Deployment

- [ ] `python test_camera.py` → PASS
- [ ] `docker-compose up -d` → Container läuft
- [ ] Logs zeigen "Stream-Verarbeitung läuft"
- [ ] FPS > 25
- [ ] Keine ERROR im Log
- [ ] Datenbank funktioniert
- [ ] Health Check bestanden
- [ ] Telegram getestet (optional)
- [ ] Backup erstellt
- [ ] System im Produktionsmodus

---

## 🐄 System ist bereit!

Das Stallwache-System ist jetzt vollständig konfiguriert und läuft in Produktion.

**Nächste Schritte:**
1. Logs regelmäßig überwachen: `docker logs -f stallwache`
2. Backups erstellen: `cp data/stallwache.db data/stallwache.db.backup`
3. System-Updates: `docker-compose pull && docker-compose up -d`
4. Bei Problemen: Siehe Troubleshooting-Sektion oder kontaktiere stallwache123@gmail.com

---

**Version**: 1.0.0  
**Status**: Production Ready ✅  
**Erstellt**: Mai 2026
