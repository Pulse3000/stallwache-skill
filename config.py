"""
Stallwache Configuration Module
Zentrale Konfiguration für alle Systemparameter
"""

import os
from pathlib import Path
from typing import Optional

# =======================
# CAMERA CONFIGURATION
# =======================

# RTSP-Stream-Einstellungen
# Rollei Safetycam HD 20 @ 192.168.178.108:80 (HTTP Port)
# RTSP Port: 554 (Standard)
CAMERA_RTSP_URL = os.getenv(
    "CAMERA_RTSP_URL",
    "rtsp://192.168.178.108:554/stream"
)
CAMERA_USERNAME = os.getenv("CAMERA_USERNAME", "Stallwache123!")
CAMERA_PASSWORD = os.getenv("CAMERA_PASSWORD", "Stallwache123!")

# Stream-Verarbeitung
FRAME_SKIP = int(os.getenv("FRAME_SKIP", "1"))  # Jedes N-te Frame verarbeiten
RESIZE_WIDTH = int(os.getenv("RESIZE_WIDTH", "1280"))
RESIZE_HEIGHT = int(os.getenv("RESIZE_HEIGHT", "720"))
BUFFER_SIZE = int(os.getenv("BUFFER_SIZE", "30"))  # Frames in Puffer

# =======================
# AI MODEL CONFIGURATION
# =======================

# YOLOv8 Modell
YOLO_MODEL_PATH = os.getenv(
    "YOLO_MODEL_PATH",
    "./models/yolov8m.pt"  # medium model, guter Kompromiß
)

# Detektions-Parameter
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.65"))
IOU_THRESHOLD = float(os.getenv("IOU_THRESHOLD", "0.45"))

# Classes (COCO-Standardklassen)
# Für Custom-Training: indices anpassen
DETECTABLE_CLASSES = {
    "cow": 21,      # COCO class index für Kuh
    "calf": 21,     # Annahme: Kalb unter gleicher Klasse
    "person": 0,    # Optional: Farmer-Erkennung
}

# =======================
# TELEGRAM CONFIGURATION
# =======================

ENABLE_TELEGRAM = os.getenv("ENABLE_TELEGRAM", "true").lower() == "true"
TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN",
    ""  # Setze via Environment Variable oder .env
)
TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID",
    ""  # Chat-ID für Alerts
)

# Telegram Alert-Verhalten
TELEGRAM_SEND_IMAGE = os.getenv("TELEGRAM_SEND_IMAGE", "true").lower() == "true"
TELEGRAM_BATCH_ALERTS = int(os.getenv("TELEGRAM_BATCH_ALERTS", "1"))  # Alerts pro Nachricht
TELEGRAM_ALERT_COOLDOWN = int(os.getenv("TELEGRAM_ALERT_COOLDOWN", "60"))  # Sekunden

# =======================
# DATABASE CONFIGURATION
# =======================

ENABLE_DATABASE = os.getenv("ENABLE_DATABASE", "true").lower() == "true"
DATABASE_PATH = Path(os.getenv(
    "DATABASE_PATH",
    "./data/stallwache.db"
))
LOG_RETENTION_DAYS = int(os.getenv("LOG_RETENTION_DAYS", "30"))

# =======================
# METRICS & MONITORING
# =======================

ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"
PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", "8000"))
METRICS_INTERVAL = int(os.getenv("METRICS_INTERVAL", "30"))  # Sekunden

# =======================
# LOGGING CONFIGURATION
# =======================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # DEBUG, INFO, WARNING, ERROR
LOG_DIR = Path(os.getenv(
    "LOG_DIR",
    "./logs"
))
LOG_MAX_SIZE = int(os.getenv("LOG_MAX_SIZE", "10485760"))  # 10MB
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))

# =======================
# SYSTEM CONFIGURATION
# =======================

DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
DEVICE = os.getenv("DEVICE", "cpu")  # 'cpu', 'cuda', 'mps'
NUM_WORKERS = int(os.getenv("NUM_WORKERS", "4"))

# Performance
MAX_QUEUE_SIZE = int(os.getenv("MAX_QUEUE_SIZE", "100"))
STREAM_TIMEOUT = int(os.getenv("STREAM_TIMEOUT", "30"))  # Sekunden
INFERENCE_TIMEOUT = int(os.getenv("INFERENCE_TIMEOUT", "5"))  # Sekunden

# =======================
# FEATURE FLAGS
# =======================

FEATURE_MULTI_CAMERA = os.getenv("FEATURE_MULTI_CAMERA", "false").lower() == "true"
FEATURE_CLOUD_BACKUP = os.getenv("FEATURE_CLOUD_BACKUP", "false").lower() == "true"
FEATURE_WEB_DASHBOARD = os.getenv("FEATURE_WEB_DASHBOARD", "false").lower() == "true"

# =======================
# VALIDATION & SETUP
# =======================

def validate_config() -> bool:
    """Validiere kritische Konfigurationsparameter."""
    errors = []

    # RTSP-URL prüfen
    if not CAMERA_RTSP_URL:
        errors.append("CAMERA_RTSP_URL nicht gesetzt")

    # Telegram (optional aber empfohlen)
    if ENABLE_TELEGRAM:
        if not TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN nicht gesetzt (aber ENABLE_TELEGRAM=true)")
        if not TELEGRAM_CHAT_ID:
            errors.append("TELEGRAM_CHAT_ID nicht gesetzt (aber ENABLE_TELEGRAM=true)")

    # YOLOv8 Modell-Datei
    if not Path(YOLO_MODEL_PATH).exists():
        errors.append(f"YOLOv8-Modell nicht gefunden: {YOLO_MODEL_PATH}")

    # Verzeichnisse erstellen
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    if errors:
        for error in errors:
            print(f"❌ Konfigurationsfehler: {error}")
        return False

    return True


# Konfiguration validieren beim Import
if __name__ != "pytest":
    # Nicht validieren wenn Tests laufen
    pass
