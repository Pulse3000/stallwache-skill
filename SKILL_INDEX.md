# 📑 Stallwache Skill - Kompletter Index

Eine vollständige Übersicht aller Dateien, ihre Zweck, und wie man sie nutzt.

---

## 🎯 Quick Navigation

### 🏃 "Ich will schnell anfangen!"
→ Lese: **DEPLOY_NOW.md** (3 Minuten)  
→ Lese: **SKILL.md** Sektion "Schritt-für-Schritt Deployment"

### 🔧 "Ich will technische Details verstehen"
→ Lese: **README.md** (vollständige Doku)  
→ Lese: **SKILL_STRUCTURE.txt** (Architektur)

### 🆘 "Ich habe Probleme!"
→ Lese: **SKILL.md** Sektion "Troubleshooting"  
→ Lese: **QUICKSTART.md** (detailliertes Setup)

### 📚 "Ich will alles überblicken"
→ Lese: **SKILL_INSTALLATION.md** (dieser Index)  
→ Lese: **FILES_OVERVIEW.md**

---

## 📁 Dateistruktur

```
stallwache/
│
├─ SKILL-Dateien (Das Herz der Skill)
│  ├─ SKILL.md ⭐ (3.500 Zeilen - Hauptdokumentation)
│  └─ evals.json (3 Test-Cases mit Assertions)
│
├─ Skill-Dokumentation (Für Skill-Nutzer & Entwickler)
│  ├─ SKILL_INSTALLATION.md ← Diese Datei
│  ├─ SKILL_README.md (Skill-Struktur-Erklärung)
│  ├─ SKILL_STRUCTURE.txt (Detaillierte Komponenten-Übersicht)
│  └─ SKILL_INDEX.md ← Navigation Guide
│
├─ Benutzer-Dokumentation (Für Produktions-Nutzer)
│  ├─ 00_LESE_MICH_ZUERST.txt (Willkommensnachricht)
│  ├─ DEPLOY_NOW.md ⭐ (3-Minuten Start)
│  ├─ START.md (Quick Overview)
│  ├─ QUICKSTART.md ⭐ (5-Minuten Detailliertes Setup)
│  └─ README.md ⭐ (Vollständige Dokumentation)
│
├─ Hardware-Dokumentation (Für Rollei-Kamera-Nutzer)
│  ├─ SETUP_ROLLEI.md (Integration Guide)
│  ├─ Rollei_HD20_Hardware_Setup_Guide.html (HTML-Version)
│  └─ Rollei_HD20_Hardware_Setup_Guide.md (Markdown-Version)
│
├─ Projekt-Übersicht (Für Projekt-Manager & Überblick)
│  ├─ PROJEKT_SUMMARY.txt (Projekt-Statistiken)
│  ├─ FILES_OVERVIEW.md (Alle 26 Dateien erklärt)
│  ├─ CHECKLIST.txt (Deployment-Checkliste)
│  └─ READY_TO_DEPLOY.md (Production Readiness)
│
├─ Python-Code (8 Module, ~1.160 Zeilen)
│  ├─ main.py (Haupteinstiegspunkt - 180 Zeilen)
│  ├─ config.py (Konfiguration - 130 Zeilen)
│  ├─ stream_processor.py (RTSP-Verarbeitung - 160 Zeilen)
│  ├─ detector.py (YOLOv8 KI - 190 Zeilen)
│  ├─ telegram_client.py (Telegram-Integration - 140 Zeilen)
│  ├─ database.py (SQLite Logging - 210 Zeilen)
│  ├─ logger.py (Logging - 80 Zeilen)
│  └─ metrics.py (Performance - 70 Zeilen)
│
├─ Docker & Deployment
│  ├─ Dockerfile (Container-Definition)
│  ├─ docker-compose.yml (Orchestrierung)
│  ├─ deploy.sh (Automation Script)
│  ├─ requirements.txt (Python-Dependencies)
│  ├─ .env.example (Konfiguration-Template)
│  └─ .env.production (DEINE produktive Config)
│
└─ Testing & Monitoring
   ├─ test_camera.py (Kamera-Validierung)
   └─ health_check.sh (System-Monitoring)
```

---

## 📖 Datei-Beschreibungen (Detailliert)

### 🎯 SKILL-DATEIEN (Kern der Skill)

#### **SKILL.md** (3.500 Zeilen) ⭐⭐⭐
- **Zweck**: Hauptdokumentation, wird in Claude geladen wenn die Skill verwendet wird
- **Inhalt**:
  - Überblick & Was macht Stallwache?
  - Anforderungen vor dem Start
  - 5-Phasen Deployment Guide (Vorbereitung, Setup, Validierung, Deployment, Verifikation)
  - System-Architektur & Komponenten
  - Python-Module Übersicht
  - Häufige Befehle
  - 10+ Troubleshooting Lösungen
  - Post-Deployment Checkliste
- **Leser**: Alle Claude-Nutzer die die Skill verwenden
- **Best For**: Wenn du die Skill bei Claude eingeben, wird dies geladen

#### **evals.json** (Test-Cases)
- **Zweck**: Automatisierte Test-Cases für Skill-Validierung
- **Inhalt**:
  - Test-Case 1: Complete Deployment (5 Assertions)
  - Test-Case 2: Camera Integration Troubleshooting (4 Assertions)
  - Test-Case 3: Performance Optimization (5 Assertions)
- **Leser**: Skill-Entwickler, Test-Automation
- **Best For**: Validierung dass Skill korrekt funktioniert

---

### 📚 SKILL-DOKUMENTATION (Für Skill-Nutzer)

#### **SKILL_INSTALLATION.md** ← LESE DIES ZUERST (für Skill-Nutzer)
- **Zweck**: How-to Guide für Skill-Installation und -Verwendung
- **Inhalt**:
  - Was ist die Skill?
  - Installation (3 Optionen: Marketplace, Manuell, GitHub)
  - Wie man die Skill nutzt (3 Szenarien)
  - Skill-Triggering Beispiele
  - Schritt-für-Schritt Anleitung
  - FAQ
  - Support Kontakt
- **Leser**: Neuer Nutzer der die Skill installieren will
- **Best For**: Erste Orientierung

#### **SKILL_README.md**
- **Zweck**: Erklärt die Skill-Paketstruktur
- **Inhalt**:
  - Dateistruktur
  - Was ist eine Skill?
  - 3 Nutzungs-Optionen
  - Skill-Evaluierung (evals.json)
  - Update-Prozess
  - Nächste Schritte
- **Leser**: Skill-Entwickler, Administrator
- **Best For**: Wenn du die Skill intern verwalten oder weiterentwickeln willst

#### **SKILL_STRUCTURE.txt**
- **Zweck**: Detaillierte Komponenten-Übersicht
- **Inhalt**:
  - Skill-Paket Übersicht
  - Zweck & automatisches Triggering
  - Alle Dateien mit Zweck
  - Code-Module Erklärungen
  - Docker & Deployment Details
  - Konfiguration
  - Test & Monitoring
  - Qualitätskriterien
  - Deployment-Ablauf
  - Statistiken
- **Leser**: Techniker, Entwickler
- **Best For**: Deep-Dive in die Architektur

#### **SKILL_INDEX.md** (Diese Datei!)
- **Zweck**: Navigation Guide für alle Dateien
- **Inhalt**: Übersicht + Index aller Dateien
- **Leser**: Jeder der sich orientieren will
- **Best For**: "Was soll ich jetzt lesen?"

---

### 📖 BENUTZER-DOKUMENTATION (Für Produktions-Nutzer)

#### **00_LESE_MICH_ZUERST.txt**
- **Zweck**: Willkommensnachricht & Navigation
- **Inhalt**:
  - Willkommen
  - 3-Minuten Schnellstart
  - Was sollte ich zuerst lesen?
  - Was ist enthalten?
  - Los geht's!
- **Leser**: Neu erstellte Nutzer
- **Best For**: Erste Schritte

#### **DEPLOY_NOW.md** ⭐ (3 Minuten)
- **Zweck**: Schnellste Möglichkeit zum Running System
- **Inhalt**:
  - Deine Konfiguration (bereits vorgesetzt!)
  - 3-Minuten Start (Schritt 1-3)
  - Häufige Befehle
  - Troubleshooting
  - Finale Checkliste
- **Leser**: Impatiente Nutzer
- **Best For**: "Ich will JETZT deployen!"

#### **START.md**
- **Zweck**: 3-Minuten Quick Overview
- **Inhalt**:
  - Überblick
  - Links zu allen Docs
  - System Info
- **Leser**: Nutzer die Überblick brauchen
- **Best For**: Navigiere zu richtigem Doc

#### **QUICKSTART.md** ⭐ (5 Minuten)
- **Zweck**: Detailliertes Setup mit Troubleshooting
- **Inhalt**:
  - Phase-by-Phase Setup
  - Kamera-Konfiguration
  - Telegram-Setup (detailed!)
  - Häufige Befehle
  - Troubleshooting
  - Monitoring
  - Checkliste
- **Leser**: Nutzer die Details wollen
- **Best For**: "Wie mache ich das genau?"

#### **README.md** ⭐ (Vollständig)
- **Zweck**: Umfassende Dokumentation
- **Inhalt**:
  - Überblick
  - Features
  - Installation & Setup
  - Konfiguration (alle 30+ Parameter)
  - API & Module
  - Monitoring & Logging
  - Troubleshooting
  - Performance Optimization
  - Backup & Recovery
- **Leser**: Technik-Profis
- **Best For**: Alles wissen

---

### 🎥 HARDWARE-DOKUMENTATION (Rollei-spezifisch)

#### **SETUP_ROLLEI.md**
- **Zweck**: Rollei Safetycam HD 20 Integration
- **Inhalt**:
  - Hardware Überblick
  - Netzwerk-Setup
  - IP-Adressierung
  - RTSP-Stream Aktivieren
  - Telegram Bot Einrichtung (detailliert!)
  - Sicherheit & Passwort
  - Häufige Probleme
- **Leser**: Rollei-Kamera-Nutzer
- **Best For**: "Ich habe eine Rollei, wie configur ich sie?"

#### **Rollei_HD20_Hardware_Setup_Guide.html**
- **Zweck**: Hardware-Handbuch (Styled HTML)
- **Inhalt**:
  - Hardware Spezifikationen
  - Netzwerk-Konfiguration
  - IP-Zuweisung
  - DDNS Setup
  - Stream-Einstellungen
  - Troubleshooting
  - Sicherheit
- **Leser**: Visuelle Lerner
- **Best For**: "Zeig mir mit schönem Layout!"

#### **Rollei_HD20_Hardware_Setup_Guide.md**
- **Zweck**: Hardware-Handbuch (Markdown)
- **Inhalt**: Gleich wie HTML-Version
- **Leser**: Text-Leser
- **Best For**: Einfacher Text mit Struktur

---

### 📊 PROJEKT-ÜBERSICHT (Meta-Information)

#### **PROJEKT_SUMMARY.txt**
- **Zweck**: Projekt-Statistiken & Überblick
- **Inhalt**:
  - Status: ✅ 100% komplett
  - 26 Dateien Übersicht
  - Code-Statistiken
  - Performance-Erwartungen
  - Checklisten
- **Leser**: Manager, Überblick-Seeker
- **Best For**: "Was ist in diesem Projekt enthalten?"

#### **FILES_OVERVIEW.md**
- **Zweck**: Komplette Dateiübersicht
- **Inhalt**:
  - Alle 26 Dateien erklärt
  - Größen & Statistiken
  - Empfohlene Lese-Reihenfolge
  - Produktiv-Checklist
- **Leser**: Nutzer die alles verstehen wollen
- **Best For**: "Wo ist welche Datei?"

#### **CHECKLIST.txt**
- **Zweck**: Deployment-Checkliste
- **Inhalt**:
  - Phase-by-Phase Verifikation
  - Häufige Befehle
  - Häufige Fehler
  - Schnell-Referenz
- **Leser**: Nutzer bei Deployment
- **Best For**: "Hab ich alles gemacht?"

#### **READY_TO_DEPLOY.md**
- **Zweck**: Production Readiness Check
- **Inhalt**:
  - Finale Checkliste
  - Performance-Verifikation
  - Security Checks
  - Backup Strategie
  - Go-Live Procedures
- **Leser**: Vor Production-Deployment
- **Best For**: "Ist das System ready?"

---

## 💻 PYTHON-CODE

### Core Logic (3 Module)

#### **main.py** (180 Zeilen)
- Haupteinstiegspunkt
- Orchestriert alle Komponenten
- Signal-Handling für Graceful Shutdown
- Error Recovery

#### **config.py** (130 Zeilen)
- Zentrale Konfiguration
- 30+ Environment-Variablen
- Validierung beim Import
- Fallback zu Defaults

#### **logger.py** (80 Zeilen)
- Logging mit Rotating File Handlers
- Farbige Console-Ausgabe
- Error & Main Log Separation

### Video & AI Processing (2 Module)

#### **stream_processor.py** (160 Zeilen)
- RTSP-Stream-Verarbeitung
- Thread-Safe Frame Queue
- Auto-Reconnect bei Fehlern
- Latenz-Optimierung

#### **detector.py** (190 Zeilen)
- YOLOv8 Inferenz-Wrapper
- Kalberkennungs-Logik
- Temporal Analysis über Frames
- Confidence-basiertes Filtering

### Integration & Logging (3 Module)

#### **telegram_client.py** (140 Zeilen)
- Telegram Bot Integration
- Alert-Versand mit Bildern
- Cooldown-Management
- Error Handling

#### **database.py** (210 Zeilen)
- SQLite Datenbank Manager
- Event-Logging
- Detektions-Protokollierung
- Auto-Cleanup (nach 30 Tagen)

#### **metrics.py** (70 Zeilen)
- Performance Monitoring
- FPS-Tracking
- Inferenz-Zeit Messung
- Uptime Calculation

---

## 🐳 DOCKER & DEPLOYMENT

#### **Dockerfile**
- Multi-stage Build
- Python 3.10 Base
- Health Check
- Non-root User (Security)
- Production-optimiert

#### **docker-compose.yml**
- One-Command Deployment
- Service: stallwache
- Volumes für Persistierung
- Resource Limits
- Health Checks
- Auto-Restart

#### **deploy.sh**
- Bash Automation
- Pre-flight Checks
- Build & Deployment
- Logging

#### **requirements.txt**
- Python Dependencies
- Version-Pinning
- Reproducibility

#### **.env.example**
- Konfiguration-Template
- Alle Parameter dokumentiert

#### **.env.production**
- DEINE produktive Config
- Mit Credentials BEREITS VORGESETZT!
- Ready to use

---

## 🧪 TESTING & MONITORING

#### **test_camera.py**
- Kamera-Verbindung validieren
- 5 Tests (network_http, http_interface, rtsp, etc.)
- Detaillierte Error Messages
- Pre-Deployment Check (MUSS PASS sein)

#### **health_check.sh**
- System Health Monitoring
- Container Status
- Network Checks
- Database Validation
- Disk Space
- Performance Metrics

---

## 🗺️ NAVIGATION NACH ANWENDUNGSFALL

### "Ich bin Anfänger und will schnell starten"
1. Lies: **00_LESE_MICH_ZUERST.txt**
2. Lies: **DEPLOY_NOW.md** (3 Minuten)
3. Führe aus: Befehle aus DEPLOY_NOW.md
4. Fertig!

### "Ich bin Techniker und will Details"
1. Lies: **README.md** (vollständig)
2. Schau: **main.py** (Kontrollfluss)
3. Schau: **detector.py** (KI-Logik)
4. Konfiguriere: **.env.production**
5. Deploye: `docker-compose up -d`

### "Ich habe Probleme beim Setup"
1. Lies: **SKILL.md** Troubleshooting
2. Führe aus: `python test_camera.py`
3. Lies: **QUICKSTART.md** detailliert
4. Prüfe: `docker logs stallwache`
5. Kontaktiere: stallwache123@gmail.com

### "Ich will das System optimieren"
1. Lies: **README.md** Performance Section
2. Lies: **SKILL.md** Troubleshooting "Hohe CPU"
3. Ändere: Parameter in **.env.production**
4. Teste: `docker-compose up -d`
5. Überwache: `docker stats stallwache`

### "Ich will als Skill-Entwickler arbeiten"
1. Lies: **SKILL_README.md**
2. Lies: **SKILL_STRUCTURE.txt**
3. Bearbeite: **SKILL.md**
4. Teste: **evals.json** Test-Cases
5. Verpacke: Als `.skill` Datei

---

## 🎯 TOP 5 DATEIEN

Falls du nur 5 Dateien lesen kannst, hier sind die wichtigsten:

1. **SKILL.md** - Alles über die Skill
2. **DEPLOY_NOW.md** - 3-Minuten zum laufen System
3. **README.md** - Vollständige Referenz
4. **main.py** - Verständnis des Code-Flows
5. **docker-compose.yml** - Verständnis von Deployment

---

## ✅ Checkliste: "Habe ich alles?"

- [ ] SKILL.md gelesen (Hauptdoku)
- [ ] DEPLOY_NOW.md gelesen (Quick Start)
- [ ] evals.json überprüft (Test-Cases)
- [ ] Python-Code vorhanden (8 Module)
- [ ] Docker-Config vorhanden (Dockerfile + compose)
- [ ] .env.production gesetzt (mit Credentials)
- [ ] test_camera.py läuft (Validierung)
- [ ] health_check.sh läuft (Monitoring)
- [ ] Dokumentation vollständig (alle .md Dateien)
- [ ] Ready to Deploy!

---

## 📞 Support

Falls du Fragen hast:

1. **Lies zuerst** die relevante Dokumentation
2. **Suche** in Troubleshooting-Sektion
3. **Führe aus**: `bash health_check.sh`
4. **Kontaktiere**: stallwache123@gmail.com

---

**🐄 Viel Erfolg mit Stallwache!**

Version: 1.0.0 | Status: Production Ready ✅ | Mai 2026
