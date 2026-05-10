# 🚀 Stallwache Skill - Installation & Verwendung

Diese Datei erklärt, wie man die **Stallwache Skill** installiert und nutzt.

---

## 📋 Was ist die Stallwache Skill?

Die **Stallwache Skill** ist ein produktionsreifes, wiederverwendbares Paket zur Bereitstellung eines KI-gesteuerten Rinderkalberkennungs-Systems. Die Skill kann in Claude (Web, Desktop, oder Cowork) installiert werden und wird automatisch angeboten, wenn der Nutzer über relevante Themen spricht.

### Was kann die Skill?

Die Skill bietet **vollständige Anleitung** für:

✅ Setup einer produktiven KI-Rinderkalberkennungs-Lösung  
✅ RTSP-Stream-Verarbeitung von IP-Kameras  
✅ YOLOv8-basierte Echtzeit-Objekterkennung  
✅ Telegram-Alerts mit Bildversand  
✅ Docker-Deployment und Orchestrierung  
✅ SQLite-Datenbank für Event-Logging  
✅ Performance-Monitoring und Health-Checks  
✅ Systematische Fehlerbehebung  
✅ Hardware-spezifische Konfiguration (Rollei Safetycam HD 20)  

---

## 🛠️ Installation

### Option 1: Cowork Skill Marketplace (Empfohlen)

1. Öffne **Cowork** auf deinem Computer
2. Gehe zu **Skills** → **Browse Marketplace**
3. Suche nach: **"Stallwache"** oder **"Cattle Monitoring"**
4. Klick auf **"Install"**
5. Die Skill ist jetzt verfügbar

Die Skill wird jetzt automatisch angeboten, wenn du über Viehüberwachung oder ähnliches sprichst.

### Option 2: Manuelles Hinzufügen (für Entwickler)

Falls du die Skill lokal testen möchtest:

```bash
# Skill-Verzeichnis kopieren
cp -r ./Stallwache ~/.cowork/skills/

# Oder im Terminal verwenden
export SKILL_PATH="./Stallwache"
claude --with-skill $SKILL_PATH "Help me set up cattle monitoring"
```

### Option 3: Direkt aus GitHub/Repository

Falls die Skill in einem Repository verteilt wird:

```bash
git clone https://github.com/xxxx/stallwache-skill.git
cd stallwache-skill
# Dann Option 1 oder 2 folgen
```

---

## 📖 Wie man die Skill nutzt

### Szenario 1: Neuer Benutzer will Stallwache deployen

1. **Öffne Cowork** (oder claude.ai)
2. **Schreib**: "Ich will ein KI-System zur Kalberkennungs-Überwachung aufsetzen. Ich habe eine Rollei Kamera an IP 192.168.178.108 und will Telegram-Alerts."
3. **Claude erkennt die Anfrage** und bietet die Stallwache Skill an
4. **Klick "Try it"** oder lass Claude die Skill nutzen
5. **Folge den Anweisungen** Schritt-für-Schritt

### Szenario 2: Troubleshooting

1. **Problem beschreiben**: "Mein RTSP-Stream funktioniert nicht, ich bekomme 'Connection timeout'"
2. Claude nutzt die Skill automatisch
3. **Bekommst systematische Fehlersuche** mit konkreten Befehlen

### Szenario 3: Performance-Optimierung

1. **Frag**: "Mein System nutzt 85% CPU, wie kann ich das optimieren?"
2. Claude bietet Tuning-Optionen aus der Skill an
3. **Bekommst konkrete Parameter** zum Einstellen

---

## 📚 Skill-Inhalt (Übersicht)

Die Skill enthält:

### 🎯 Hauptdokumentation (SKILL.md)
- Überblick und Was-macht-Stallwache
- 5-Phasen Deployment-Guide (vom Start bis Production)
- System-Architektur
- Komponenten-Beschreibungen
- 10+ häufige Probleme & Lösungen
- Post-Deployment Checkliste

### 💻 Produktiver Code (8 Python-Module)
- main.py - Haupteinstiegspunkt
- config.py - Konfigurationsmanagement
- stream_processor.py - RTSP-Stream-Verarbeitung
- detector.py - YOLOv8 KI-Detektion
- telegram_client.py - Telegram-Integration
- database.py - SQLite Event-Logging
- logger.py - Logging & Monitoring
- metrics.py - Performance-Metriken

### 🐳 Deployment (Docker + Scripts)
- Dockerfile - Production Container
- docker-compose.yml - One-Command Deployment
- deploy.sh - Automation Script
- requirements.txt - Python Dependencies
- .env.production - Konfigurationsdatei (mit Credentials vorgesetzt)

### 🧪 Tests & Monitoring
- test_camera.py - Kamera-Validierung
- health_check.sh - System-Monitoring

### 📖 Zusätzliche Dokumentation
- DEPLOY_NOW.md - 3-Minuten Start-Guide
- QUICKSTART.md - 5-Minuten Detailliertes Setup
- README.md - Vollständige Dokumentation
- SETUP_ROLLEI.md - Rollei-spezifische Integration
- Rollei_HD20_Hardware_Setup_Guide - Hardware-Handbuch (HTML + Markdown)
- CHECKLIST.txt - Deployment-Checkliste
- FILES_OVERVIEW.md - Komplette Dateiübersicht

---

## ⚙️ Skill-Triggering

Die Skill wird **automatisch angeboten**, wenn du über folgende Themen fragst:

| Nutzer sagt... | Claude erkennt | Angebot |
|---|---|---|
| "Ich will Kalbungen automatisch erkennen" | Cattle monitoring | Skill wird angeboten |
| "Wie deploye ich ein AI-System für Tiere?" | Animal detection | Skill wird angeboten |
| "Ich habe eine IP-Kamera und will Alerts" | IoT monitoring | Skill wird angeboten |
| "Docker deployment für Viehüberwachung" | Livestock + Docker | Skill wird angeboten |
| "Echtzeit-Objekt-Erkennung für meinen Stall" | Real-time + Animals | Skill wird angeboten |
| "Telegram Alerts für Notfälle im Stall" | Farm + Alerts | Skill wird angeboten |

Die Skill ist **super flexibel** und wird auch erkannt, wenn du anders formulierst.

---

## 🎯 Schritt-für-Schritt Anleitung (für Anfänger)

### 1. Vorbereitung (5 Minuten)

Sammle diese Informationen:
- ✓ Kamera IP-Adresse (z.B. 192.168.178.108)
- ✓ Kamera-Credentials (Username & Password)
- ✓ RTSP-URL (z.B. rtsp://192.168.178.108:554/stream)
- ✓ (Optional) Telegram Bot Token und Chat-ID

### 2. Skill aktivieren

Öffne Claude und schreib:
```
Ich will ein automatisches Kalberkennungs-System aufsetzen.
Ich habe die Kamera IP 192.168.178.108:80, 
Username: Stallwache123!, 
Password: Stallwache123!
Und ich bin bereit für Production-Deployment mit Docker.
```

### 3. Folge den Anweisungen

Claude wird dir jetzt **Schritt-für-Schritt Anweisungen** geben:

1. Teste deine Kamera: `python test_camera.py`
2. Richte Telegram ein (optional)
3. Erstelle .env.production
4. Starte Docker: `docker-compose up -d`
5. Überwache Logs: `docker logs -f stallwache`
6. Verifikation: `bash health_check.sh`

### 4. System läuft! 🎉

Nach ~5 Minuten läuft dein System 24/7 und sendet Kalbungs-Alerts!

---

## 🔄 Skill Updates & Maintenance

### Skill aktualisieren

Wenn eine neue Version verfügbar ist:

1. Öffne Cowork
2. Gehe zu **Skills**
3. Suche "Stallwache"
4. Klick **"Update"** (falls ein Update verfügbar ist)

### Skill konfigurieren

Die meisten Nutzer werden die Skill **"out of the box"** verwenden können. Falls du Custom-Konfiguration brauchst:

1. Siehe `.env.production` für alle Optionen
2. Passe die Werte nach deinen Anforderungen an
3. Neustarten: `docker-compose restart stallwache`

### Skill deinstallieren

Falls du die Skill nicht mehr brauchst:

1. Öffne Cowork
2. Gehe zu **Skills**
3. Suche "Stallwache"
4. Klick **"Uninstall"**

---

## 📞 Support & Hilfe

### Häufige Fragen

**F: Muss ich etwas programmieren?**  
A: Nein! Die Skill bietet alle Befehle, die du kopieren und einfügen kannst.

**F: Kann ich das System anpassen?**  
A: Ja! Siehe `.env.production` für 30+ Konfigurationsoptionen.

**F: Was kostet die Skill?**  
A: Die Skill ist kostenlos. Du zahlst nur für:
- Docker (kostenlos)
- Claude API-Nutzung (falls über API genutzt)
- Deine Hardware

**F: Funktioniert das mit anderen Kameras?**  
A: Ja! Jede RTSP-fähige IP-Kamera funktioniert. Die Skill ist Kamera-agnostisch.

**F: Kann ich mehrere Kameras anschließen?**  
A: Aktuell 1 Kamera. Mehrere Kameras sind auf der Roadmap (FEATURE_MULTI_CAMERA Flag).

### Kontakt

**Email**: stallwache123@gmail.com

Falls du Probleme hast:
1. Lies die Troubleshooting-Sektion in SKILL.md
2. Führe `bash health_check.sh` aus
3. Prüfe `docker logs stallwache`
4. Kontaktiere den Support

---

## 📊 Skill-Statistiken

- **Skill-Dateien**: SKILL.md, evals.json
- **Dokumentation**: 9 Dateien, ~15.000 Wörter
- **Python-Code**: 8 Module, ~1.160 Zeilen
- **Test-Cases**: 3 umfassende Evaluierungen
- **Deployment**: Docker, Automation Scripts
- **Status**: ✅ Production Ready
- **Version**: 1.0.0
- **Erstellt**: Mai 2026

---

## 🎓 Lernen & Weiterentwicklung

Falls du mehr über die Technologie lernen möchtest:

### Videos & Tutorials
- YOLOv8 Detektion: [Ultralytics Docs](https://docs.ultralytics.com)
- Docker Best Practices: [Docker Official Docs](https://docs.docker.com)
- Telegram Bot API: [Telegram Bot Docs](https://core.telegram.org/bots/api)

### Code-Verständnis
- Lies `README.md` für Architektur-Überblick
- Schau `main.py` für den Kontrollfluss an
- Lies `detector.py` für KI-Logik

### Modifications & Custom Use-Cases
Falls du die Skill erweitern möchtest, kontaktiere uns oder öffne einen Pull Request.

---

## ✅ Checkliste nach Installation

- [ ] Skill in Cowork installiert oder lokal verfügbar
- [ ] SKILL.md Datei accessible
- [ ] evals.json Test-Cases vorhanden
- [ ] Python-Code-Module vorhanden
- [ ] Docker-Config vorgesetzt
- [ ] Dokumentation lesbar
- [ ] Test-Scripts funktionsfähig

---

## 🚀 Los geht's!

Die Stallwache Skill ist bereit zur Verwendung. Starten Sie jetzt:

1. Installiere die Skill (Cowork Marketplace oder manuell)
2. Öffne Claude/Cowork
3. Beschreib dein Rinderkalberkennungs-Projekt
4. Lass die Skill die Arbeit machen! 🐄

---

**Viel Erfolg mit deinem Stallwache-System!**

Version: 1.0.0 | Status: Production Ready ✅ | Erstellt: Mai 2026
