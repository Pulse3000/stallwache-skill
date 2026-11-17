# 🎥 Stallwache + Rollei Safetycam HD 20 Setup Guide

Dieses Dokument beschreibt die komplette Integration zwischen deiner Rollei Safetycam HD 20 und dem Stallwache KI-System.

**Deine Kamera-Infos:**
```
Kamera-ID: 006E07844083
DDNS-Domain: stallwache.rolleicam.net
Firmware: 87.2.64.174
DDNS-Status: ✓ Erfolgreich
Verbindung: Kabelgebunden (Ethernet)
```

---

## 🚀 Quickstart (5 Minuten)

### 1. RTSP-Stream testen

```bash
# Im gleichen Netzwerk (LAN)
vlc "rtsp://admin:12345@192.168.1.200:554/stream"

# Über DDNS (Remote)
vlc "rtsp://admin:12345@stallwache.rolleicam.net:554/stream"
```

Wenn Video abgespielt wird → ✓ RTSP funktioniert

### 2. Konfiguration

```bash
cp .env.example .env.production
nano .env.production  # oder Editor öffnen
```

Setze diese kritischen Variablen:
```env
CAMERA_RTSP_URL=rtsp://192.168.1.200:554/stream
CAMERA_USERNAME=U9917104310
CAMERA_PASSWORD=!!!maskedXXX
TELEGRAM_BOT_TOKEN=6012345678:ABCDEFg...
TELEGRAM_CHAT_ID=987654321
```

### 3. Starten

```bash
# Mit Docker Compose (empfohlen)
docker-compose -f docker-compose.yml up -d

# Oder mit Bash-Script
bash deploy.sh

# Oder manuell
python main.py
```

### 4. Verify

```bash
# Logs anschauen
docker logs -f stallwache

# oder
tail -f logs/stallwache.log
```

---

## 🔧 Detaillierte Setup-Schritte

### Schritt 1: Kamera-Passwort ändern

**WICHTIG:** Ändere das Standard-Passwort von `12345`!

1. Öffne Kamera-Web-Interface:
   ```
   http://192.168.1.200  (LAN)
   oder
   https://stallwache.rolleicam.net (Remote)
   ```

2. Login mit `admin` / `12345`

3. Gehe zu: **Einstellungen → System → Benutzer**

4. Ändere Admin-Passwort zu sicherem Passwort

5. Aktualisiere `.env.production`:
   ```env
   CAMERA_PASSWORD=dein_neues_passwort
   ```

### Schritt 2: RTSP-Stream konfigurieren

1. Im Web-Interface: **Einstellungen → Video → Stream**

2. Stelle sicher:
   - **Haupt-Stream:** Aktiviert
   - **Kodierung:** H.264
   - **Auflösung:** 1920×1080 (Full HD)
   - **Framerate:** 30 fps
   - **Bitrate:** 4-6 Mbps (automatisch empfohlen)

3. RTSP-URL sollte sein:
   ```
   rtsp://[CAMERA_IP]:554/stream
   ```

### Schritt 3: DDNS konfigurieren (für Remote-Zugriff)

Deine Kamera ist bereits mit DDNS `stallwache.rolleicam.net` registriert.

Verifiziere:
1. Im Web-Interface: **Einstellungen → Netzwerk → DDNS**
2. Status sollte "Erfolgreich" sein
3. Teste: `ping stallwache.rolleicam.net`

Falls Remote-Zugriff fehlschlägt:
- Prüfe Router Port-Forwarding (Port 554/TCP → Kamera-IP)
- Prüfe Firewall

### Schritt 4: Telegram-Bot einrichten

#### 4.1 Bot-Token erstellen

1. Starte Telegram-App
2. Suche `@BotFather`
3. Schreib: `/newbot`
4. BotFather fragt nach Namen (z.B. "Stallwache Bot")
5. BotFather fragt nach Username (z.B. "stallwache_alerts_bot")
6. **Token kopieren:** `6012345678:ABCDEFg1234567890...`

#### 4.2 Chat-ID ermitteln

1. Suche deinen neuen Bot in Telegram
2. Schreib eine beliebige Nachricht
3. Öffne Terminal/CMD und führe aus:

```bash
export TOKEN="6012345678:ABCDEFg1234567890..."
curl https://api.telegram.org/bot$TOKEN/getUpdates
```

Oder (Windows):
```powershell
$TOKEN="6012345678:ABCDEFg1234567890..."
curl.exe "https://api.telegram.org/bot$TOKEN/getUpdates"
```

4. In der Antwort findest du:
```json
{
  "result": [
    {
      "message": {
        "chat": {
          "id": 987654321  ← DIESE NUMMER
        }
      }
    }
  ]
}
```

5. Setze in `.env.production`:
```env
TELEGRAM_BOT_TOKEN=6012345678:ABCDEFg1234567890...
TELEGRAM_CHAT_ID=987654321
```

#### 4.3 Bot-Berechtigungen setzen

Optional, aber empfohlen:

1. Im BotFather: `/mybots` → dein Bot
2. → **Bot Settings** → **Default Commands**
3. Setze:
   ```
   start - Starte Stallwache
   status - Zeige aktuellen Status
   help - Hilfe
   ```

### Schritt 5: Docker-Deployment

#### Option A: Docker Compose (EMPFOHLEN)

```bash
# 1. Konfiguration kopieren
cp .env.example .env.production

# 2. .env.production anpassen (Text-Editor)
nano .env.production

# 3. Starten
docker-compose -f docker-compose.yml up -d

# 4. Logs anschauen
docker-compose logs -f stallwache
```

#### Option B: Bash Deployment-Script

```bash
# 1. Konfiguration vorbereiten
cp .env.example .env.production
nano .env.production

# 2. Deploy-Script ausführen
bash deploy.sh
```

#### Option C: Manueller Start

```bash
# 1. Dependencies installieren
pip install -r requirements.txt

# 2. YOLOv8 Modell herunterladen
python -c "from ultralytics import YOLO; YOLO('yolov8m.pt')"

# 3. Umgebungsvariablen setzen
export $(cat .env.production | xargs)

# 4. Starten
python main.py
```

---

## 🔍 Troubleshooting

### "Konnte RTSP-Stream nicht öffnen"

```bash
# 1. Prüfe Netzwerk-Erreichbarkeit
ping 192.168.1.200

# 2. Teste mit VLC
vlc "rtsp://admin:12345@192.168.1.200:554/stream"

# 3. Teste RTSP-Port direkt
nc -zv 192.168.1.200 554

# 4. Prüfe Kamera-Status-Seite
# Öffne: http://192.168.1.200
# Sollte "DDNS-Status: Erfolgreich" zeigen
```

### "Telegram-Alerts funktionieren nicht"

```bash
# 1. Test Bot-Token
TOKEN="6012345678:ABCDEFg..."
curl https://api.telegram.org/bot$TOKEN/getMe

# 2. Test Nachricht senden
CHAT_ID="987654321"
curl https://api.telegram.org/bot$TOKEN/sendMessage \
  -d "chat_id=$CHAT_ID&text=Test"

# 3. Prüfe Logs
docker logs stallwache | grep -i telegram
```

### "Container läuft nicht"

```bash
# 1. Prüfe Status
docker ps -a

# 2. Siehe Fehler
docker logs stallwache

# 3. Neu starten
docker restart stallwache
```

### "Hohe CPU-Auslastung"

```bash
# In .env.production:
FRAME_SKIP=2              # Skip mehr Frames
RESIZE_WIDTH=640          # Kleinere Auflösung
RESIZE_HEIGHT=360
YOLO_MODEL_PATH=./models/yolov8n.pt  # Kleineres Modell
```

---

## 📊 Monitoring

### Live-Status

```bash
# Logs in Echtzeit
docker logs -f stallwache

# oder
tail -f logs/stallwache.log
```

### Metriken

```bash
# Prometheus Metriken
curl http://localhost:8000/metrics

# oder
curl http://localhost:8000/metrics | grep stallwache
```

### Datenbank abfragen

```bash
# SQLite Kommandozeile
sqlite3 data/stallwache.db

# Beispiele:
sqlite> SELECT * FROM events ORDER BY timestamp DESC LIMIT 10;
sqlite> SELECT COUNT(*) FROM events WHERE event_type='CALVING_DETECTED';
sqlite> SELECT AVG(fps) FROM metrics;
```

---

## 🔐 Sicherheit

### Wichtig für Production:

1. **Kamera-Passwort ändern:**
   - Standard `12345` → sicheres Passwort
   - In `.env.production` aktualisieren

2. **RTSP-Port schützen:**
   - Nur im LAN exponieren
   - oder VPN für Remote-Zugriff verwenden

3. **Telegram-Token schützen:**
   - **NIEMALS** in Logs committen
   - `.env` zu `.gitignore` hinzufügen

4. **Datenbank-Backup:**
   ```bash
   cp data/stallwache.db data/stallwache.db.backup
   ```

5. **Firewall-Regeln:**
   ```bash
   # Nur LAN auf Port 554 (RTSP)
   ufw allow from 192.168.1.0/24 to any port 554
   
   # Nur lokale Metriken (Port 8000)
   ufw allow from 127.0.0.1 to any port 8000
   ```

---

## 🎯 Production Checklist

- [ ] Kamera-Passwort geändert
- [ ] RTSP-Stream getestet (VLC)
- [ ] Telegram Bot erstellt & Chat-ID ermittelt
- [ ] `.env.production` konfiguriert
- [ ] Docker Compose / Deploy-Script getestet
- [ ] Logs überprüft (keine Fehler)
- [ ] Telegram-Test Alert erhalten
- [ ] Database funktioniert (sqlite3 abfrage)
- [ ] Metriken-Endpoint erreichbar
- [ ] Firewall-Regeln gesetzt
- [ ] Git `.env` zu `.gitignore` hinzugefügt
- [ ] Datenbank-Backup erstellt

---

## 📞 Support

**Probleme?**

1. Prüfe `logs/stallwache.log` auf Fehler
2. Teste RTSP manuell mit VLC
3. Prüfe Telegram Bot-Token & Chat-ID
4. Docker Container Logs: `docker logs stallwache`

**Kontakt:** stallwache123@gmail.com

---

## 📚 Weiterführende Ressourcen

- [Rollei Safetycam HD 20 Manual](http://rollei.net)
- [YOLOv8 Dokumentation](https://docs.ultralytics.com)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Docker Dokumentation](https://docs.docker.com)

---

**🐄 Viel Erfolg mit Stallwache!**
