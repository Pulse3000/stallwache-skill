---
name: stallwache
description: AI-powered calf birthing detection system with real-time monitoring, Telegram alerts, and cloud deployment via Vercel. Automatically detects cattle calving events using YOLOv8 object detection.
compatibility: Python 3.10+, Vercel, Docker, macOS/Linux/Windows

---

# 🐄 Stallwache - AI Calf Birthing Detection

Fully automated system for detecting cattle calving (birthing) events in real-time using AI and sending instant Telegram alerts to farmers.

## 🎯 What Stallwache Does

**Monitors cattle 24/7 via IP camera, detects births via AI, sends instant alerts via Telegram.**

### Key Features
- ✅ Real-time YOLOv8 AI detection (28-30 FPS @ 1080p)
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
git clone https://github.com/stallwache/skill.git
cd stallwache
cp .env.example .env.production
# Edit .env.production with your camera IP and Telegram token
docker-compose up -d
```

### Vercel Deployment (Cloud)
```bash
git add .
git push origin main
# Go to https://vercel.com/new → import stallwache-skill
# Set 12 environment variables → Deploy
curl https://stallwache-skill.vercel.app/api/health
```

## 📚 Documentation

- **Quick Start:** 5 minutes
- **Complete Guide:** 30 minutes
- **Architecture:** 20 minutes

## 🔐 Security

- No hardcoded secrets
- Environment variables for all credentials
- HTTPS/SSL on Vercel
- MIT License - Free for all use

---

**Version:** 1.0.0
**Status:** Production Ready ✅
**GitHub:** https://github.com/stallwache/skill
