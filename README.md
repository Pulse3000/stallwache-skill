# 🐄 Stallwache - KI-basiertes Kalberkennungssystem

Vollautomatisches, produktionsreifes System zur Echtzeitüberwachung von Kühen und automatischer Erkennung von Kalbungen.

**Features:**
- ✅ RTSP-Stream-Verarbeitung (Rollei HD 20 & kompatibel)
- ✅ YOLOv8 Echtzeit-Inferenz
- ✅ Telegram-Alerts mit Bildern
- ✅ SQLite-Datenbanklogging
- ✅ Performance-Metriken & Monitoring
- ✅ Docker-Support für Production Deployment
- ✅ Fehlertoleranz & Auto-Recovery

---

## 📦 Installation

### 1. Requirements installieren

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 2. YOLOv8-Modell herunterladen

```bash
python -c "from ultralytics import YOLO; YOLO('yolov8m.pt')"
```

Das Modell wird automatisch zu `~/.local/models/yolov8m.pt` heruntergeladen.

### 3. Konfiguration

Kopiere `.env.example` zu `.env` und setze deine Parameter:

```bash
cp .env.example .env
```

**Kritische Variablen:**
```env
CAMERA_RTSP_URL=rtsp://192.168.1.200:554/stream
CAMERA_USERNAME=admin
CAMERA_PASSWORD=12345
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

## 🚀 Quickstart

### Lokales Starten

```bash
python main.py
```

### Mit Docker

```bash
# Build
docker build -t stallwache:latest .

# Run
docker run -d \
  --name stallwache \
  -e CAMERA_RTSP_URL=rtsp://192.168.1.200:554/stream \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e TELEGRAM_CHAT_ID=your_chat_id \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/data:/app/data \
  stallwache:latest
```

### Docker Compose

```bash
docker-compose up -d
```

---

## 📋 Systemkomponenten

### `main.py`
Haupteinstiegspunkt. Orchestriert alle Komponenten.

```python
system = StallwacheSystem()
system.run()
```

### `config.py`
Zentrale Konfiguration. Alle Parameter können über Environment-Variablen gesetzt werden.

### `stream_processor.py`
RTSP-Stream-Verarbeitung mit Thread-sicheren Queues:
- Automatisches Reconnect bei Ausfällen
- Frame-Buffering für glatte Verarbeitung
- Latenz-Optimierung

### `detector.py`
YOLOv8-basierte Kalberkennungs-Inferenz:
- Real-time object detection
- Temporal analysis (Konsistenz über mehrere Frames)
- Konfidenz-Scoring

### `telegram_client.py`
Telegram-Integration mit Alerts:
- Automatische Alerts bei Erkennung
- Bild-Versand (optional)
- Cooldown-Steuerung (verhindert Alert-Spam)
- Status-Updates

### `database.py`
SQLite-Datenbanklogging:
- Event-Protokollierung
- Detektions-Logging
- Performance-Metriken
- Automatisches Aufräumen (ältere Einträge)

### `metrics.py`
Performance-Monitoring:
- FPS-Tracking
- Inferenz-Zeit-Messung
- Uptime-Monitoring

---

## 🔧 Konfiguration

### Umgebungsvariablen

```bash
# Camera
CAMERA_RTSP_URL=rtsp://admin:12345@192.168.1.200:554/stream
FRAME_SKIP=1                    # Jedes N-te Frame verarbeiten
RESIZE_WIDTH=1280
RESIZE_HEIGHT=720

# AI
YOLO_MODEL_PATH=./models/yolov8m.pt
CONFIDENCE_THRESHOLD=0.65       # Min. Konfidenz
IOU_THRESHOLD=0.45

# Telegram
ENABLE_TELEGRAM=true
TELEGRAM_BOT_TOKEN=123456789:ABCDefg...
TELEGRAM_CHAT_ID=987654321
TELEGRAM_SEND_IMAGE=true
TELEGRAM_ALERT_COOLDOWN=60      # Sekunden zwischen Alerts

# Database
ENABLE_DATABASE=true
DATABASE_PATH=./data/stallwache.db
LOG_RETENTION_DAYS=30

# Logging
LOG_LEVEL=INFO                  # DEBUG, INFO, WARNING, ERROR
LOG_DIR=./logs

# System
DEBUG_MODE=false
DEVICE=cpu                      # cpu, cuda, mps
STREAM_TIMEOUT=30
```

---

## 📊 Monitoring & Logs

### Logs
```
logs/
├── stallwache.log           # Hauptlog
└── stallwache_error.log     # Nur Fehler
```

### Datenbank
```
data/stallwache.db          # SQLite mit Events & Metriken
```

### Console Output
```
2024-01-15 10:23:45 | main | INFO | Starte Stream-Verarbeitung...
2024-01-15 10:24:12 | detector | WARNING | 🚨 KALBUNG ERKANNT! Confidence: 78.5% | Frame: 1284
2024-01-15 10:24:13 | telegram_client | INFO | ✓ Telegram-Alert gesendet | CALVING
```

---

## 🧪 Testing

Unit-Tests ausführen:
```bash
pytest tests/ -v
```

Mit Coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

---

## 🐛 Troubleshooting

### Problem: "Konnte RTSP-Stream nicht öffnen"
**Lösung:**
```bash
# Test mit VLC
vlc "rtsp://admin:12345@192.168.1.200:554/stream"

# Prüfe Netzwerk
ping 192.168.1.200
```

### Problem: "YOLOv8-Modell nicht gefunden"
**Lösung:**
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8m.pt')"
mkdir -p models
mv ~/.local/models/yolov8m.pt ./models/
```

### Problem: Telegram-Alerts funktionieren nicht
**Lösung:**
```bash
# Test Bot-Token
curl https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe

# Prüfe Chat-ID
echo "Send a message to the bot, then:"
curl https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates
```

### Problem: Hohe CPU-Auslastung
**Lösung:**
```env
# In .env:
FRAME_SKIP=2              # Skip mehr Frames
RESIZE_WIDTH=640          # Kleinere Auflösung
RESIZE_HEIGHT=360
DEVICE=cuda               # GPU falls vorhanden
```

---

## 📈 Performance-Optimierung

### CPU-Optimierung
```env
FRAME_SKIP=2              # Jedes 2. Frame
YOLO_MODEL_PATH=./models/yolov8n.pt  # nano statt medium
DEVICE=cpu
```

### GPU-Beschleunigung (CUDA)
```bash
# Install CUDA Version (siehe ultralytics docs)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# In .env:
DEVICE=cuda
```

### Production-Tipps
- Run in Docker für Isolation & Reproducibility
- Verwende Read-only `/app` Volume für Code
- Mount separate Volumes für logs & data
- Health-Check: Container prüft Metriken-Endpunkt
- Skalierung: Multi-Camera Support über Umgebungsvariablen

---

## 📚 API-Integration

### Database Queries

```python
from database import Database

db = Database()
db.initialize()

# Hole Kalbungs-Events
calving_events = db.get_calving_events(days=7)
for event in calving_events:
    print(f"{event['timestamp']} - Confidence: {event['confidence']}")

# Hole Metriken
metrics = db.get_metrics_summary(hours=24)
print(f"Avg FPS: {metrics['avg_fps']:.1f}")
```

### Custom Alerts

```python
from telegram_client import TelegramClient

client = TelegramClient()
client.send_alert(
    event_type="CALVING",
    confidence=0.85,
    frame_number=1234,
    frame_image=cv_frame
)
```

---

## 🔐 Sicherheit

- ✅ Passwort nicht in Logs (Environment-Variables)
- ✅ Datenbank ist lokal (keine Cloud ohne Encryption)
- ✅ RTSP-Credentials in URL (nicht in Logs)
- ✅ Telegram Bot-Token in `.env` (nicht committen!)
- ✅ Read-only File-Permissions für Code

**Git Setup:**
```bash
echo ".env" >> .gitignore
git add .gitignore
```

---

## 📝 Lizenz

MIT License - Siehe LICENSE Datei

---

## 👨‍💼 Support

Fragen? Kontakt: **stallwache123@gmail.com**

---

## 🔄 Version History

### v1.0.0 (2024-01-15)
- ✅ Initial Release
- ✅ RTSP-Stream Processing
- ✅ YOLOv8 Inference
- ✅ Telegram Integration
- ✅ Database Logging
- ✅ Docker Support
