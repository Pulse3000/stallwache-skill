# 🐄 STALLWACHE - PRODUCTION SYSTEM

## ⚡ 3-Minuten Start

```bash
# 1. Kamera validieren (30 Sekunden)
python test_camera.py

# 2. System starten (1 Minuten)
docker-compose up -d

# 3. Status prüfen (Logs anschauen)
docker logs -f stallwache
```

**Das wars! System läuft jetzt.** ✅

---

## 📖 Dokumentation (nach Bedarf)

| Du möchtest... | Öffne... | Dauer |
|---|---|---|
| **Schnell starten** | `QUICKSTART.md` | 5 min |
| **Alles verstehen** | `README.md` | 15 min |
| **Kamera einrichten** | `SETUP_ROLLEI.md` | 10 min |
| **Hardware Details** | `Rollei_HD20_Hardware_Setup_Guide.html` | - |
| **Dateien Übersicht** | `FILES_OVERVIEW.md` | 5 min |
| **Production Checklist** | `READY_TO_DEPLOY.md` | 5 min |

---

## ✅ Konfiguration

Deine Kamera ist bereits konfiguriert:
```env
CAMERA_RTSP_URL=rtsp://192.168.178.108:554/stream
CAMERA_USERNAME=admin
CAMERA_PASSWORD=12345
```

**Optional - Telegram Alerts aktivieren:**

Öffne `.env.production` und setze:
```env
TELEGRAM_BOT_TOKEN=dein_token
TELEGRAM_CHAT_ID=deine_chat_id
```

Dann neu starten: `docker-compose down && docker-compose up -d`

---

## 🚀 Starten & Monitoring

```bash
# System starten
docker-compose up -d

# Logs anschauen (live)
docker logs -f stallwache

# Status prüfen
bash health_check.sh

# System stoppen
docker-compose down
```

---

## 🔧 Bei Problemen

```bash
# 1. Kamera testen
python test_camera.py

# 2. Logs prüfen
docker logs stallwache | grep -i error

# 3. Health Check
bash health_check.sh

# 4. Siehe QUICKSTART.md → Troubleshooting
```

---

## 📞 Hilfe

| Problem | Lösung |
|---------|--------|
| **Kamera antwortet nicht** | `python test_camera.py` |
| **Container startet nicht** | `docker logs stallwache` |
| **Telegram nicht aktiv** | Siehe SETUP_ROLLEI.md Punkt 4 |
| **Datenbank Error** | Prüfe `data/` Verzeichnis Rechte |

**Siehe auch:** QUICKSTART.md → Troubleshooting Sektion

---

## 🎯 Nächste Schritte nach Start

1. **Monitor** die Logs für ~5 Minuten
   - Sollte "Stream-Verarbeitung läuft" sehen
   - Sollte FPS-Metriken sehen

2. **Test** die Kalbungs-Erkennung
   - Zeige Kuh-Video vor Kamera
   - Sollte Alert bekommen

3. **Kalibriere** Konfidenz-Schwelle
   - In `config.py`: `CONFIDENCE_THRESHOLD`
   - Standard: 0.65 (65%)

---

## 📊 System Info

```
🐄 Projekt: Stallwache - KI-basierte Kalberkennungs-System
📷 Kamera: Rollei Safetycam HD 20 @ 192.168.178.108:80
🤖 AI-Modell: YOLOv8 Medium (Object Detection)
💾 Datenbank: SQLite3 (Events, Metriken)
📱 Alerts: Telegram Bot
🐳 Deployment: Docker Container
⚙️ Status: Production Ready ✅
```

---

**🚀 Los geht's! Öffne Terminal und starten Sie mit:**

```bash
python test_camera.py
docker-compose up -d
docker logs -f stallwache
```

---

*Erstellt: Mai 2026 | Version: 1.0.0 | Status: Production Ready*

**Fragen? Siehe FILES_OVERVIEW.md oder README.md** 📚
