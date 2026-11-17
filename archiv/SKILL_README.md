# Stallwache Skill - Paketstruktur

Dieses Verzeichnis enthält die **Stallwache Skill** - ein produktionsreifes System für KI-basierte Kalberkennungs-Überwachung.

## 📋 Dateistruktur

```
stallwache/
├── SKILL.md                           ← Hauptdokumentation (Skill-Inhalt)
├── SKILL_README.md                    ← Diese Datei
├── evals.json                         ← Test-Cases für Skill-Evaluierung
│
├── 00_LESE_MICH_ZUERST.txt           ← Schnellstart (Deutsch)
├── DEPLOY_NOW.md                      ← 3-Minuten Deployment Guide
├── START.md                           ← Quick Overview
├── QUICKSTART.md                      ← 5-Minuten Setup
├── README.md                          ← Vollständige Dokumentation
├── SETUP_ROLLEI.md                    ← Rollei Kamera Integration
├── FILES_OVERVIEW.md                  ← Dateiübersicht
├── CHECKLIST.txt                      ← Deployment Checklist
├── PROJEKT_SUMMARY.txt                ← Projekt-Statistik
├── READY_TO_DEPLOY.md                 ← Production Readiness
│
├── Python Core (8 Module)
│   ├── main.py                        ← Haupteinstiegspunkt (180 Zeilen)
│   ├── config.py                      ← Konfiguration (130 Zeilen)
│   ├── stream_processor.py            ← RTSP-Verarbeitung (160 Zeilen)
│   ├── detector.py                    ← YOLOv8 KI (190 Zeilen)
│   ├── telegram_client.py             ← Telegram-Integration (140 Zeilen)
│   ├── database.py                    ← SQLite (210 Zeilen)
│   ├── logger.py                      ← Logging (80 Zeilen)
│   └── metrics.py                     ← Performance (70 Zeilen)
│
├── Docker & Deployment
│   ├── Dockerfile                     ← Container-Definition
│   ├── docker-compose.yml             ← Orchestrierung
│   ├── deploy.sh                      ← Automatisierung
│   ├── requirements.txt               ← Python-Abhängigkeiten
│   ├── .env.example                   ← Konfiguration-Template
│   └── .env.production                ← Produktive Config (mit Credentials)
│
├── Testing & Monitoring
│   ├── test_camera.py                 ← Kamera-Validierung
│   └── health_check.sh                ← System-Monitoring
│
├── Hardware Setup
│   ├── Rollei_HD20_Hardware_Setup_Guide.html
│   └── Rollei_HD20_Hardware_Setup_Guide.md
```

## 🎯 Was ist eine Skill?

Eine Skill ist ein **wiederverwendbares Paket** von Anweisungen, Code-Templates und Best-Practices, das Claude in Cowork automatisch als Hilfe anbietet. Diese Stallwache-Skill:

1. **Wird automatisch angeboten**, wenn ein Nutzer über Kalberkennungs-, Viehüberwachungs- oder KI-Monitoring-Systeme spricht
2. **Enthält vollständige Anleitung** für Deployment und Troubleshooting
3. **Kann in Cowork installiert werden** für schnelle, wiederholte Deployments
4. **Ist wartbar und erweiterbar** - Updates sind einfach zu verbreiten

## 📖 Wie man diese Skill nutzt

### Option 1: Als Entwickler (lokal testen)

```bash
# Skill-Verzeichnis laden
export SKILL_PATH="./Stallwache"

# Test mit Claude durchführen
claude --with-skill $SKILL_PATH
```

### Option 2: In Cowork installieren

1. Skill-Verzeichnis zu Cowork Skills hinzufügen
2. Claude bietet die Skill automatisch an
3. Nutzer können sie mit einem Klick verwenden

### Option 3: Als .skill-Datei verpacken

```bash
# Skill in .skill-Datei konvertieren (ZIP-Archiv)
zip -r stallwache.skill stallwache/
mv stallwache.skill stallwache.skill.zip
```

## ✅ Skill-Evaluierung

Die `evals.json` Datei enthält Test-Cases für die Skill-Validierung:

### Test-Case 1: Complete Deployment
- **Szenario**: Benutzer hat Hardware und will System deployen
- **Erwartung**: Schritt-für-Schritt Anleitung vom Start bis zur Produktion
- **Assertions**: Kamera-Validierung, Telegram-Setup, Docker-Befehle, Verification

### Test-Case 2: Camera Integration
- **Szenario**: RTSP-Stream funktioniert nicht
- **Erwartung**: Systematische Fehlersuche mit Befehlen
- **Assertions**: Netzwerk-Diagnostik, RTSP-Tools, Config-Verify

### Test-Case 3: Performance Optimization
- **Szenario**: CPU-Auslastung zu hoch
- **Erwartung**: Tuning-Optionen mit Trade-offs
- **Assertions**: Frame-Skip, Modell-Sizing, Resolution, Trade-offs

## 🔄 Skill-Update-Prozess

Um die Skill zu aktualisieren:

1. **SKILL.md bearbeiten** - Anweisungen aktualisieren
2. **evals.json aktualisieren** - Tests anpassen falls nötig
3. **Test durchführen**:
   ```bash
   claude --with-skill ./Stallwache
   # Durch evals.json Test-Cases durchgehen
   ```
4. **In Cowork deployen** - Skill in Marketplace hochladen

## 📊 Skill-Statistiken

- **Dokumentation**: ~3.500 Zeilen SKILL.md
- **Zusatzdokumentation**: ~15.000 Wörter (README, SETUP, etc.)
- **Python-Code**: ~1.160 Zeilen (8 Module)
- **Test-Cases**: 3 umfassende Evaluierungen
- **Deployment-Optionen**: Docker, Automation, Health Checks

## 🚀 Nächste Schritte

### Für Nutzer:
1. Öffne SKILL.md (oder lass Claude die Skill automatisch anbieten)
2. Folge den Anweisungen
3. Deploye mit `docker-compose up -d`

### Für Entwickler:
1. Bearbeite SKILL.md für Improvements
2. Aktualisiere evals.json für neue Test-Cases
3. Führe Tests durch
4. Packe als .skill-Datei für Distribution

## 📞 Support

**Kontakt**: stallwache123@gmail.com

**Repository**: Diese Skill wurde erstellt am 4. Mai 2026 für die Stallwache v1.0.0 Initiative.

---

**Version**: 1.0.0  
**Status**: Production Ready ✅  
**Format**: Cowork Skill (YAML frontmatter + Markdown)
