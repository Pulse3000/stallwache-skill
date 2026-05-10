# 🚀 STALLWACHE - DEPLOY NOW!

**Status: ✅ BEREIT ZUM STARTEN**

---

## 📋 Deine aktuelle Konfiguration

```
✅ Kamera IP:          192.168.178.108:80
✅ RTSP Stream:        rtsp://192.168.178.108:554/stream
✅ Username:           Stallwache123!
✅ Password:           Stallwache123!
✅ DDNS:               stallwache.rolleicam.net
✅ Kamera-ID:          006E07844083
✅ Status:             Alle Credentials gesetzt ✓
```

---

## ⚡ 3-MINUTEN START

### Schritt 1: Kamera validieren (30 Sekunden)

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

Falls **FAIL** → siehe Troubleshooting unten

### Schritt 2: System starten (1-2 Minuten)

```bash
# Starten
docker-compose up -d

# Prüfen
docker ps | grep stallwache

# Sollte zeigen:
# stallwache  ... Up 5 seconds
```

### Schritt 3: Logs überwachen (1 Minute)

```bash
docker logs -f stallwache
```

**Erwartet in Logs:**
```
✓ YOLOv8-Modell erfolgreich geladen
✓ RTSP-Stream-Processor initialisiert
✓ SQLite-Datenbank initialisiert
✓ Telegram-Client initialisiert (falls aktiviert)
🎬 Starte Stream-Verarbeitung...
📊 Performance | FPS: 28.5 | Frames: 300 | Alerts: 0
```

---

## 🎉 FERTIG!

**System läuft jetzt!** 🐄

---

## 📱 Optional: Telegram Aktivieren

Falls du Alerts zu Telegram bekommen möchtest:

### Schritt 1: Telegram Bot erstellen (5 Minuten)

1. Öffne Telegram App
2. Suche: `@BotFather`
3. Schreib: `/newbot`
4. Bot-Name: z.B. "Stallwache Alerts"
5. Username: z.B. "stallwache_bot"
6. **Token kopieren:** `6012345678:ABCDEFg1234567890...`

### Schritt 2: Chat-ID ermitteln

1. Schreib eine Nachricht an deinen neuen Bot
2. Terminal:
```bash
export TOKEN="6012345678:ABCDEFg..."
curl https://api.telegram.org/bot$TOKEN/getUpdates
```

3. In der JSON-Antwort: `"id": 987654321` = deine Chat-ID

### Schritt 3: Konfigurieren

```bash
nano .env.production
```

Setze:
```env
ENABLE_TELEGRAM=true
TELEGRAM_BOT_TOKEN=6012345678:ABCDEFg...
TELEGRAM_CHAT_ID=987654321
```

Speichern und Neu starten:
```bash
docker-compose down
docker-compose up -d
```

---

## 🔧 Häufige Befehle

```bash
# Logs anschauen (live)
docker logs -f stallwache

# Logs anschauen (letzte 100 Zeilen)
docker logs --tail 100 stallwache

# System stoppen
docker-compose down

# System neu starten
docker-compose restart stallwache

# Health Check
bash health_check.sh

# Datenbank abfragen
sqlite3 data/stallwache.db "SELECT COUNT(*) FROM events;"

# Metriken prüfen
curl http://localhost:8000/metrics
```

---

## 🆘 Wenn etwas schief geht

### Problem: "test_camera.py FAIL"

```bash
# 1. Ping zur Kamera
ping 192.168.178.108

# 2. Prüfe mit VLC
vlc "rtsp://Stallwache123!:Stallwache123!@192.168.178.108:554/stream"

# 3. Prüfe .env.production
cat .env.production | grep CAMERA
```

### Problem: "Container startet nicht"

```bash
# Logs prüfen
docker logs stallwache

# Container neu bauen
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Problem: "Kein Stream geladen"

```bash
# Credentials prüfen in .env.production
CAMERA_USERNAME=Stallwache123!
CAMERA_PASSWORD=Stallwache123!

# RTSP-URL prüfen
CAMERA_RTSP_URL=rtsp://192.168.178.108:554/stream
```

### Problem: "Telegram funktioniert nicht"

```bash
# Bot-Token testen
TOKEN="dein_token"
curl https://api.telegram.org/bot$TOKEN/getMe

# Nachricht testen
CHAT_ID="deine_chat_id"
curl https://api.telegram.org/bot$TOKEN/sendMessage \
  -d "chat_id=$CHAT_ID&text=Test"
```

---

## 📊 System Monitor

**Während System läuft:**

```bash
# Real-time Status
watch 'docker ps | grep stallwache; echo "---"; docker stats --no-stream stallwache'

# oder

# Health Check
bash health_check.sh

# Sollte zeigen:
# ✓ Container läuft
# ✓ Kamera erreichbar
# ✓ Metriken OK
# ✓ Datenbank OK
```

---

## 🎯 Nach dem Start (erste 30 Minuten)

1. **Beobachte die Logs** (15 Minuten)
   - Sollte konstant FPS-Metriken zeigen
   - Sollte keine Fehler haben

2. **Teste die Kalbungserkennung**
   - Zeige ein Kuh-Video vor Kamera
   - System sollte erkennen & Alert senden (falls Telegram aktiv)

3. **Prüfe die Datenbank**
   ```bash
   sqlite3 data/stallwache.db "SELECT * FROM events LIMIT 5;"
   ```
   - Sollte Events anzeigen

4. **Erstelle ein Backup**
   ```bash
   cp data/stallwache.db data/stallwache.db.backup
   ```

---

## ✅ Finale Checkliste

- [ ] `python test_camera.py` → ✓ PASS
- [ ] `docker-compose up -d` → Container läuft
- [ ] Logs zeigen "Stream-Verarbeitung läuft"
- [ ] FPS > 25
- [ ] Keine ERROR im Log
- [ ] Datenbank funktioniert
- [ ] Health Check bestanden
- [ ] Telegram getestet (optional)

---

## 🚀 ALL SET!

**Das System ist jetzt bereit für 24/7 Betrieb!**

```bash
# Starten
docker-compose up -d

# Logs anschauen
docker logs -f stallwache

# Fertig! 🎉
```

---

## 📞 Deine Kontaktinformationen

```
Email: stallwache123@gmail.com
Projekt: Stallwache v1.0.0
Status: PRODUCTION READY ✅
```

---

**🐄 Los geht's! System läuft jetzt!**
