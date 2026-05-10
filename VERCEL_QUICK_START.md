# ⚡ Stallwache Vercel - Quick Start (3 Minuten)

## 1️⃣ Push zu GitHub

```bash
cd C:\Users\axe2k\Desktop\Projekt\ Stall\stallwache\Stallwache
git add .
git commit -m "feat: Add Vercel deployment"
git push origin main
```

Oder:
```powershell
.\auto_deploy.ps1
```

---

## 2️⃣ Vercel Connect

1. Gehe zu: **https://vercel.com/new**
2. Melde Dich mit GitHub an
3. Wähle: **stallwache-skill**
4. Klicke: **Import**

---

## 3️⃣ Environment Variables setzen

In Vercel Dashboard, füge diese Variables in "Environment Variables" hinzu:

```
CAMERA_RTSP_URL = rtsp://admin:PASSWORD@192.168.178.108/stream
CAMERA_USERNAME = admin
CAMERA_PASSWORD = YOUR_PASSWORD
TELEGRAM_BOT_TOKEN = YOUR_TOKEN
TELEGRAM_CHAT_ID = YOUR_CHAT_ID
ENABLE_TELEGRAM = true
DEVICE = cpu
YOLO_MODEL_PATH = ./models/yolov8m.pt
CONFIDENCE_THRESHOLD = 0.65
FRAME_SKIP = 1
LOG_LEVEL = INFO
LOG_RETENTION_DAYS = 30
```

---

## 4️⃣ Deploy!

Klicke: **Deploy**

Warte: 1-3 Minuten

Fertig! 🎉

---

## 5️⃣ Test deine API

Öffne in Browser:
```
https://stallwache-skill.vercel.app/api/health
```

Du solltest sehen:
```json
{
  "status": "healthy",
  "version": "1.0.0-vercel"
}
```

---

## 🔗 API Endpoints

| Endpoint | Beschreibung |
|----------|-------------|
| `/api/health` | Health Check |
| `/api/status` | Current Status |
| `/api/events?hours=24` | Events der letzten 24 Stunden |
| `/api/statistics?days=30` | Statistiken der letzten 30 Tage |
| `/api/config` | Konfiguration (ohne Secrets) |

---

## ✅ Fertig!

Deine Stallwache API läuft jetzt in der Cloud:
```
https://stallwache-skill.vercel.app
```

---

**Für Details siehe: `VERCEL_DEPLOYMENT_COMPLETE.md`**
