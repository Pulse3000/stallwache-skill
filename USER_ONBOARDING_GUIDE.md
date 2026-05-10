# 🎓 User Onboarding Guide - Stallwache

Leitfaden für neue Nutzer zur schnellen Orientierung und zum erfolgreichen Start.

---

## 👋 Willkommen bei Stallwache!

Du hast die beste Entscheidung für deine Rinder-Überwachung getroffen! 🐄

Dieses Onboarding-Programm wird dich in **30 Minuten** von Anfänger zu produktivem Nutzer bringen.

---

## 🎯 Deine Reise (3 Phasen)

### Phase 1: Understanding (10 Minuten)
✓ Was ist Stallwache?
✓ Wie funktioniert das System?
✓ Was benötige ich?

### Phase 2: Setup (15 Minuten)
✓ Kamera-Konfiguration
✓ System-Deployment
✓ Erste Tests

### Phase 3: Mastery (5 Minuten)
✓ Monitoring starten
✓ Alerts konfigurieren
✓ Erste Erkenntnisse

---

## 📖 PHASE 1: Understanding (10 Minuten)

### 1.1 Was ist Stallwache? (2 Min)

Stallwache ist ein **KI-System, das automatisch Kalbungen erkennt**.

```
Wie es funktioniert:

1. Kamera filmt die Kühe 24/7
2. AI-Modell (YOLOv8) verarbeitet Video in Echtzeit
3. Wenn Kalb erkannt → ALERT!
4. Du bekommst Telegram-Nachricht mit Foto
5. Du kannst sofort handeln
```

### 1.2 Benefits (3 Min)

✅ **Automatisch**: Keine manuellen Checks nötig
✅ **Zuverlässig**: 28-30 FPS @ 1080p
✅ **Schnell**: ~2 Sekunden bis zum Alert
✅ **24/7**: Rund um die Uhr Überwachung
✅ **Einfach**: "docker-compose up -d" und fertig
✅ **Günstig**: Kostenlos, Open Source
✅ **Privat**: Deine Daten bleiben lokal

### 1.3 Was brauchst du? (2 Min)

Technisch:
- 💻 Standard PC/Laptop/NUC
- 📷 IP-Kamera mit RTSP (z.B. Rollei Safetycam)
- 🌐 Internets
- 🐳 Docker (kostenlos)

Optional:
- 📱 Telegram (kostenlos)
- ☁️ Cloud-Backup (deine Wahl)

### 1.4 Wie viel Zeit? (3 Min)

```
Einmalig:
  Setup: 30 Minuten
  Konfiguration: 15 Minuten
  Testing: 10 Minuten
  ═══════════════
  Total: 55 Minuten

Laufend:
  Monitoring: ~2 Min/Woche (optionales Backup)
  Wartung: 1x/Monat (logs prüfen)
```

---

## 🔧 PHASE 2: Setup (15 Minuten)

### 2.1 Vorbereitung (3 Min)

**Sammle diese Informationen:**

```
Kamera-Details:
  □ IP-Adresse: _______________
  □ RTSP-URL: _______________
  □ Username: _______________
  □ Password: _______________

Beispiel:
  IP: 192.168.1.100
  RTSP: rtsp://192.168.1.100:554/stream
  Username: admin
  Password: password123
```

### 2.2 Installation (5 Min)

**Schritt 1: Kopiere Dateien**

```bash
# Projekt-Verzeichnis erstellen
mkdir ~/stallwache
cd ~/stallwache

# Alle Dateien hier platzieren
# (von Cowork oder GitHub)
```

**Schritt 2: Konfiguriere**

```bash
# Editiere .env.production
nano .env.production

# oder mit deinem Editor öffnen
# Setze deine Kamera-Daten:
CAMERA_RTSP_URL=deine_rtsp_url
CAMERA_USERNAME=dein_username
CAMERA_PASSWORD=dein_passwort
```

**Schritt 3: Starte System**

```bash
# Docker-Container starten
docker-compose up -d

# Überprüfe Status
docker ps | grep stallwache
# Sollte zeigen: stallwache ... Up 2 seconds
```

### 2.3 Validierung (4 Min)

**Test 1: Kamera-Verbindung**

```bash
python test_camera.py

# Erwartet:
# ✓ PASS - network_http
# ✓ PASS - http_interface
# ✓ PASS - network_rtsp
# ✓ PASS - rtsp_noauth
# ✓ PASS - rtsp_auth
# ✓ ALL TESTS PASSED (5/5)
```

**Test 2: System läuft**

```bash
docker logs -f stallwache

# Erwartet:
# ✓ YOLOv8 model loaded
# ✓ RTSP processor started
# ✓ SQLite database initialized
# 🎬 Stream processing started...
# 📊 Performance | FPS: 28.5 | Frames: 300
```

**Test 3: Health Check**

```bash
bash health_check.sh

# Erwartet:
# ✓ Container running
# ✓ Camera reachable
# ✓ Database OK
# ✓ Metrics OK
```

### 2.4 Telegram Setup (3 Min) - Optional

Falls du Alerts möchtest:

```bash
# 1. Öffne Telegram → @BotFather
# 2. Schreib: /newbot
# 3. Gib einen Namen ein
# 4. BotFather gibt dir einen Token

# 5. Bekomme deine Chat-ID
export TOKEN="dein_token_hier"
curl https://api.telegram.org/bot$TOKEN/getUpdates

# 6. Setze in .env.production
TELEGRAM_BOT_TOKEN=dein_token
TELEGRAM_CHAT_ID=deine_chat_id
ENABLE_TELEGRAM=true

# 7. Neu starten
docker-compose down
docker-compose up -d
```

---

## 🚀 PHASE 3: Mastery (5 Minuten)

### 3.1 Monitoring aktivieren

```bash
# Live-Logs anschauen
docker logs -f stallwache

# Was du sehen wirst:
# [INFO] Stream processing: FPS 28.5
# [INFO] Detection: confidence 0.87
# [ALERT] Calf detected! Sending alert...
# [SENT] Telegram message sent successfully
```

### 3.2 Alerts verwalten

**Telegram Alert erhalten:**

```
🐄 STALLWACHE ALERT
━━━━━━━━━━━━━━━━━
Kalb erkannt!
Confidence: 87%
Zeit: 14:32:15
Camera: Main Barn
```

Klick auf Bild um Frame zu sehen.

### 3.3 Datenbank prüfen

```bash
# Zeige Events der letzten Stunde
sqlite3 data/stallwache.db \
  "SELECT * FROM events ORDER BY timestamp DESC LIMIT 10;"

# Statistiken
sqlite3 data/stallwache.db \
  "SELECT COUNT(*) FROM events;"
```

### 3.4 Performance prüfen

```bash
# CPU/RAM Auslastung
docker stats stallwache

# Typische Werte:
# CPU: 30-60%
# Memory: 2-3 GB
# FPS: 28-30
```

---

## 📚 Nächste Schritte nach dem Onboarding

### Kurz-Term (Diese Woche)

- [ ] System läuft 24/7
- [ ] Alerts funktionieren
- [ ] Erste Detektionen gesehen
- [ ] Backup erstellt

```bash
cp data/stallwache.db data/stallwache.db.backup
```

### Mittel-Term (Diesen Monat)

- [ ] Konfiguration optimiert
- [ ] False Positives reduziert
- [ ] Logs reviewed
- [ ] Dokumentation gelesen

### Long-Term (Dieses Jahr)

- [ ] Multi-camera Setup (v1.1)
- [ ] Web Dashboard (v1.1)
- [ ] Cloud Backup (v2.0)
- [ ] Advanced Analytics (v2.0)

---

## 🆘 Quick Help

### "Mein System zeigt keine Events"

```bash
# 1. Prüfe Kamera-Verbindung
python test_camera.py

# 2. Prüfe Logs
docker logs stallwache | grep -i "error\|fail"

# 3. Erhöhe Confidence (zu viele False Positives?)
CONFIDENCE_THRESHOLD=0.75  # Standard: 0.65

# 4. Starte neu
docker-compose restart stallwache
```

### "Zu viele False Alerts"

```bash
# Option 1: Erhöhe Confidence
CONFIDENCE_THRESHOLD=0.75

# Option 2: Erhöhe FRAME_SKIP (weniger Processing)
FRAME_SKIP=2

# Option 3: Reduziere Alert Cooldown
TELEGRAM_ALERT_COOLDOWN=120  # Weniger häufig alerts
```

### "Hohe CPU-Auslastung"

```bash
# Option 1: Weniger Frames verarbeiten
FRAME_SKIP=2  # Oder höher

# Option 2: Kleineres Modell
YOLO_MODEL_PATH=./models/yolov8s.pt

# Option 3: Niedrigere Auflösung
RESIZE_WIDTH=640
RESIZE_HEIGHT=480
```

---

## 📞 Getting Help

### Dokumentation

**START HIER:**
- 📖 DEPLOY_NOW.md (3-Minuten Start)
- 📖 QUICKSTART.md (5-Minuten Setup)
- 📖 SKILL.md (alles!)

### Community

- 🐛 GitHub Issues (Bugs/Features)
- 💬 GitHub Discussions (Questions)
- 📧 Email: stallwache123@gmail.com

---

## ✅ Onboarding Abschluss-Checklist

Gratulationen! Du hast alles gelernt. Markiere wenn fertig:

- [ ] PHASE 1 verstanden (What/Why/How)
- [ ] PHASE 2 durchgeführt (Setup/Config/Deploy)
- [ ] PHASE 3 aktiv (Monitoring/Alerts)
- [ ] Health Check bestanden
- [ ] Telegram optional konfiguriert
- [ ] Erste Erkenntnisse gesehen
- [ ] Backup erstellt

---

## 🎓 Du bist bereit!

**Glückwunsch!** Du bist jetzt:

✅ Stallwache Expert
✅ System läuft 24/7
✅ Alerts sind aktiv
✅ Datenbank protokolliert
✅ Bereit für die Kalbungszeit

**Nächster Schritt:**
👉 Starte dein System in Produktion!

---

## 💚 Feedback

Wie war dein Onboarding-Erlebnis?

📧 Email: stallwache123@gmail.com
🐛 GitHub Issue: https://github.com/stallwache/skill/issues
💬 Discussion: https://github.com/stallwache/skill/discussions

---

**🐄 Viel Erfolg mit deinen Kälbern!** 🎉

Created with ❤️ for farmers worldwide
