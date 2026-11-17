---
name: stallwache
description: AI-powered calf birthing detection system with real-time monitoring, Telegram alerts, and cloud deployment via Vercel. Automatically detects cattle calving events using YOLOv8 object detection.
compatibility: Python 3.10+, Vercel, Docker, macOS/Linux/Windows

---

# 🐄 Stallwache - AI Calf Birthing Detection

System for detecting cattle calving (birthing) events from an IP camera stream and sending Telegram alerts to farmers.

## ⚠️ Status — read this first

- **A calving alert needs a custom-trained model.** The detector reports a calving only on model evidence: class `amniotic_sac` or `calf_legs` with confidence above 0.80. The default model (`yolov8m.pt`, COCO classes) does not know these classes, so **with the default model no calving alert is ever sent** — the system logs a warning at start and stays silent. This is deliberate: "a cow next to a second object" is not evidence of a birth.
- **No trained model ships with this skill.** Training your own is a prerequisite, not an option.
- **Performance figures below are targets, not measurements** on a reference device.
- This repository is a standalone prototype. The maintained system (web app, edge agent, detection rules, roadmap) is developed in `Pulse3000/Die_Stallwache`.

## 🎯 What Stallwache Does

**Reads an IP camera stream, runs YOLOv8 on it, and sends a Telegram alert when the model reports birth evidence.**

### Key Features
- ✅ YOLOv8 inference on the camera stream
- ✅ RTSP camera stream processing
- ✅ Instant Telegram alerts with image
- ✅ Event database logging
- ✅ Docker deployment (one-command setup)
- ✅ Vercel cloud REST API endpoints
- ✅ Auto-restart on failure
- ✅ Comprehensive logging and metrics

## 🚀 Quick Start

### Docker Deployment (Local)
```bash
# 1. Clone
git clone https://github.com/Pulse3000/stallwache-skill.git
cd stallwache-skill

# 2. Configure
cp .env.example .env.production
# Edit .env.production with your camera IP and Telegram token

# 3. Deploy
docker-compose up -d
```

### Vercel Deployment (Cloud)
```bash
# 1. Push to GitHub
git add .
git push origin main

# 2. Go to https://vercel.com/new
# 3. Import stallwache-skill repo
# 4. Set 12 environment variables
# 5. Deploy

# 6. Test
curl https://stallwache-skill.vercel.app/api/health
```

## 🔧 Configuration

### Environment Variables
```
CAMERA_RTSP_URL         - RTSP stream URL
CAMERA_USERNAME         - Camera credentials
CAMERA_PASSWORD         - Camera credentials
TELEGRAM_BOT_TOKEN      - Telegram bot token
TELEGRAM_CHAT_ID        - Telegram chat ID
ENABLE_TELEGRAM         - true/false
DEVICE                  - cpu or cuda
YOLO_MODEL_PATH         - Model file path
CONFIDENCE_THRESHOLD    - 0.0-1.0
FRAME_SKIP              - Skip N frames
LOG_LEVEL               - DEBUG/INFO/WARNING/ERROR
LOG_RETENTION_DAYS      - Days to keep logs
```

## 📊 System Architecture

```
RTSP Camera Stream
       ↓
Stream Processor (RTSP)
       ↓
YOLOv8 Detector (AI)
       ↓
Event Logger (SQLite)
       ↓
├─ Telegram Alert (if detected)
├─ Database Entry
└─ Metrics Update
```

## 🌐 REST API Endpoints (Vercel)

| Endpoint | Purpose |
|----------|---------|
| GET /api/health | Health check |
| GET /api/status | Current status |
| GET /api/events?hours=24 | Detection events |
| GET /api/statistics?days=30 | Statistics |
| GET /api/config | Configuration |

## 🔐 Security

- No hardcoded secrets
- Environment variables for all credentials
- HTTPS/SSL on Vercel
- Optional API key authentication
- Configurable CORS

## 📈 Performance (targets, not measured)

These figures are design targets. They have not been measured on a reference
device and depend on hardware, model size and stream resolution.

- **Processing:** 28-30 FPS @ 1080p (GPU class hardware)
- **Detection Latency:** <100ms
- **Alert Delivery:** <2 seconds

## 📚 Documentation

- **Quick Start:** 5 minutes
- **Complete Guide:** 30 minutes
- **Architecture:** 20 minutes
- **Troubleshooting:** Full coverage

## 🎓 Learn More

- GitHub: https://github.com/Pulse3000/stallwache-skill
- Documentation: See project files
- Support: stallwache123@gmail.com

## 📄 License

MIT License - Free for personal, research, and commercial use

## 🙏 Credits

Built with ❤️ for farmers and AI enthusiasts.

---

**Version:** 1.0.0
**Status:** Prototype — calving alerts require a custom-trained model (see "Status" above)
**Last Updated:** May 2026
