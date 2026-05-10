# 📦 Stallwache Skill - Packaging Guide

Anleitung zum Erstellen der `.skill`-Datei für Cowork Distribution.

---

## 📁 .skill Datei-Struktur

Eine `.skill`-Datei ist ein ZIP-Archive mit dieser Struktur:

```
stallwache.skill (ZIP-Archive)
│
├─ SKILL.md ← ERFORDERLICH (3.500 Zeilen Dokumentation)
├─ evals.json ← ERFORDERLICH (Test-Cases mit Assertions)
│
├─ references/ (Optional aber empfohlen)
│  ├─ troubleshooting.md
│  ├─ architecture.md
│  └─ deployment-checklist.md
│
├─ scripts/ (Optional aber empfohlen)
│  ├─ setup_skill.sh
│  ├─ deploy_stallwache.sh
│  └─ validate_setup.py
│
├─ assets/ (Optional)
│  ├─ docker-compose-template.yml
│  ├─ .env-template
│  └─ config-examples.json
│
└─ README.md (Optional, Marketplace-Beschreibung)
```

---

## 🛠️ Schritt-für-Schritt Anleitung

### Option 1: Manuell mit ZIP-Tool

```bash
# 1. Erstelle ein neues Verzeichnis
mkdir stallwache-skill-package
cd stallwache-skill-package

# 2. Kopiere die erforderlichen Dateien
cp ../SKILL.md .
cp ../evals.json .

# 3. Erstelle das ZIP-Archive
zip -r stallwache.skill SKILL.md evals.json

# 4. Umbenennen (optional, für Klarheit)
mv stallwache.skill stallwache-v1.0.0.skill
```

### Option 2: Mit Linux/Mac

```bash
# 1. Navigiere zum Projekt-Verzeichnis
cd ~/stallwache

# 2. Erstelle das ZIP-Archive
zip -r stallwache.skill \
  SKILL.md \
  evals.json \
  references/ \
  scripts/ \
  assets/ \
  README.md

# 3. Überprüfe das Archive
unzip -l stallwache.skill
```

### Option 3: Mit Python (Cross-Platform)

```python
import zipfile
import os

def create_skill_package(source_dir, output_file):
    """Erstelle ein .skill-Package"""
    
    required_files = [
        'SKILL.md',
        'evals.json'
    ]
    
    optional_dirs = [
        'references',
        'scripts',
        'assets'
    ]
    
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Erforderliche Dateien
        for file in required_files:
            path = os.path.join(source_dir, file)
            if os.path.exists(path):
                zf.write(path, arcname=file)
            else:
                print(f"⚠️ Warnung: {file} nicht gefunden")
        
        # Optionale Verzeichnisse
        for dir_name in optional_dirs:
            dir_path = os.path.join(source_dir, dir_name)
            if os.path.exists(dir_path):
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_dir)
                        zf.write(file_path, arcname=arcname)

# Verwendung
create_skill_package('.', 'stallwache-v1.0.0.skill')
print("✅ Skill-Package erstellt: stallwache-v1.0.0.skill")
```

---

## 📝 Marketplace-Beschreibung

Für den Cowork Marketplace brauchst du eine `README.md` mit Marketplace-Metadaten:

```markdown
# 🐄 Stallwache - KI-basiertes Kalberkennungs-System

**Version**: 1.0.0  
**Status**: Production Ready ✅  
**Autor**: Stallwache Team  
**Email**: stallwache123@gmail.com

## Überblick

Stallwache ist ein produktionsreifes, vollautomatisiertes System zur 
Erkennung von Kalbungen in Rinderbeständen mittels KI.

### Was macht Stallwache?

✅ Real-time Kalberkennungs-Erkennung via YOLOv8  
✅ RTSP-Stream-Verarbeitung von IP-Kameras  
✅ Telegram-Alerts mit Bildversand  
✅ SQLite Event-Logging  
✅ Docker-Deployment (One-Command)  
✅ 24/7 Monitoring & Health-Checks  
✅ Comprehensive Troubleshooting Guides  

### Anforderungen

- Docker & Docker-Compose
- IP-Kamera mit RTSP-Stream
- (Optional) Telegram Bot Token

### Schnellstart

```bash
# 1. Kamera testen
python test_camera.py

# 2. System starten
docker-compose up -d

# 3. Logs überwachen
docker logs -f stallwache
```

### Features

- **Production-Ready**: Getesteter Code, Container, Health-Checks
- **Comprehensive Docs**: 3.500 Zeilen SKILL.md + 13 weitere Dateien
- **Multi-Level**: Quick-Start (3 min), Standard (5 min), Expert
- **Evaluated**: 3 Test-Cases mit 14 Assertions
- **Hardware-Specific**: Rollei Safetycam HD 20 Integration

### Support

Email: stallwache123@gmail.com

---

**🐄 Viel Erfolg mit Stallwache!**
```

---

## ✅ Checkliste vor Packaging

- [ ] SKILL.md existiert (3.500 Zeilen)
- [ ] evals.json existiert (3 Test-Cases, 14 Assertions)
- [ ] SKILL.md hat YAML-Frontmatter (name, description, compatibility)
- [ ] Alle internen Links funktionieren
- [ ] Keine sensiblen Daten in .skill
- [ ] README.md existiert (Marketplace-Beschreibung)
- [ ] Version ist in Frontmatter gesetzt
- [ ] ZIP-Archive erstellt
- [ ] Archive kann mit unzip -l überprüft werden
- [ ] Größe unter 50 MB (typisch <10 MB)

---

## 📤 Upload zu Cowork Marketplace

### Schritt 1: Marketplace-Konto

1. Gehe zu Cowork Marketplace
2. Registriere dich als Creator
3. Verifiziere deine Email

### Schritt 2: Skill hochladen

1. Klick "New Skill"
2. Lade `stallwache-v1.0.0.skill` hoch
3. Fülle Metadaten ein:
   - Name: Stallwache
   - Category: Livestock / Agriculture / Monitoring
   - Tags: cattle, ai, detection, monitoring, docker
   - Description: (aus README.md)
   - Compatibility: Docker, Python 3.10+

### Schritt 3: Veröffentlichung

1. Review & Test (Marketplace-Team)
2. Genehmigung
3. Live im Marketplace! 🎉

---

## 🔄 Updates & Versioning

Für neue Versionen:

```bash
# 1. Update SKILL.md (Inhalte)
# 2. Update evals.json (Test-Cases falls nötig)
# 3. Erhöhe Version in Frontmatter
# 4. Erstelle neues .skill Package
# 5. Upload zu Marketplace

# Versionierungsschema: MAJOR.MINOR.PATCH
# Beispiel: 1.0.0 → 1.1.0 (neue Features) oder 1.0.1 (Bug-Fixes)
```

---

## 🎯 Marketplace-Metadaten Vorlage

```yaml
# Marketplace-Informationen (setzen beim Upload)

skill_name: stallwache
version: 1.0.0
category: Agriculture / Livestock
tags: [cattle, ai, detection, monitoring, docker, telegram]

author:
  name: Stallwache Team
  email: stallwache123@gmail.com
  website: https://github.com/stallwache/skill

description: |
  AI-powered calf birthing detection and cattle monitoring system.
  Production-ready with Docker, Telegram alerts, and comprehensive docs.

long_description: |
  Stallwache is a comprehensive, production-ready system for 
  detecting cattle calving events using YOLOv8 AI models...

requirements:
  - docker
  - docker-compose
  - python: ">=3.10"
  - hardware: IP-Camera with RTSP

features:
  - Real-time YOLOv8 detection
  - RTSP stream processing
  - Telegram alerts with images
  - SQLite event logging
  - 24/7 monitoring
  - Docker deployment

installation_method: cowork_marketplace
is_open_source: true
source_url: https://github.com/stallwache/skill
license: MIT

support:
  email: stallwache123@gmail.com
  github_issues: https://github.com/stallwache/skill/issues
```

---

## 📊 Package-Größen-Referenz

```
Typische .skill-Datei-Größen:

Minimal (nur SKILL.md + evals.json):
  • ~200 KB (komprimiert)

Mit References & Scripts:
  • ~500 KB (komprimiert)

Mit allen Assets & Code:
  • ~1-2 MB (komprimiert)

Stallwache-Skill (erwartet):
  • ~3-5 MB (mit all optionalen Dateien)
```

---

## 🧪 Testen des .skill Packages

Nach dem Erstellen:

```bash
# 1. Überprüfe das Archive
unzip -l stallwache-v1.0.0.skill

# 2. Extrahiere zum Testen
mkdir test-skill
unzip stallwache-v1.0.0.skill -d test-skill/

# 3. Verifiziere erforderliche Dateien
ls test-skill/SKILL.md
ls test-skill/evals.json

# 4. Überprüfe Größe
du -sh stallwache-v1.0.0.skill

# 5. Test in Cowork (falls lokal unterstützt)
cowork install test-skill/stallwache-v1.0.0.skill
```

---

## ✅ Distribution-Kanäle

### Cowork Marketplace (Primär)
- Automatische Updates
- Zentrale Verwaltung
- Community-Reviews
- Offizielle Unterstützung

### GitHub (Secondary)
- Open-Source Repo
- Community-Zugang
- Issue-Tracking
- Pull-Request-Reviews

### Direct Distribution
- Direkte Datei-Links
- Für interne Nutzung
- Custom-Anpassungen
- Enterprise-Deployment

---

**Die .skill-Datei ist dein Packaging-Format für globale Distribution!** 📦🌍

Version: 1.0.0 | Mai 2026
