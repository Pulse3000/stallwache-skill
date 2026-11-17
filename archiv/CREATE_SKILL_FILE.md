# 📦 Create .skill File - Step-by-Step

Anleitung zum Erstellen der Stallwache `.skill`-Datei für den Cowork Marketplace.

---

## 🎯 Was ist eine .skill-Datei?

Eine `.skill`-Datei ist ein **ZIP-Archive** mit allen notwendigen Dateien:
- SKILL.md (Hauptdokumentation)
- evals.json (Test-Cases)
- Konfigurationsdateien
- Python-Code
- Dokumentation

Der Marketplace lädt diese Datei hoch und Nutzer können sie mit 1 Klick installieren.

---

## 📋 VORBEREITUNG

### Schritt 1: Alle Dateien prüfen

Stelle sicher dass diese Dateien in deinem Projekt-Verzeichnis existieren:

**Erforderlich:**
- ✅ SKILL.md
- ✅ evals.json
- ✅ README.md (oder README_FOR_GITHUB.md)
- ✅ CONTRIBUTING.md
- ✅ LICENSE
- ✅ CHANGELOG.md
- ✅ requirements.txt

**Python-Code (wichtig):**
- ✅ main.py
- ✅ config.py
- ✅ stream_processor.py
- ✅ detector.py
- ✅ telegram_client.py
- ✅ database.py
- ✅ logger.py
- ✅ metrics.py

**Docker & Deployment:**
- ✅ Dockerfile
- ✅ docker-compose.yml
- ✅ .env.example

**Tests:**
- ✅ test_camera.py
- ✅ health_check.sh

**Überprüfung:**
```bash
cd ~/stallwache

# Prüfe dass alle Dateien existieren
ls -la SKILL.md evals.json README.md LICENSE requirements.txt
ls -la main.py config.py detector.py
ls -la Dockerfile docker-compose.yml
ls -la test_camera.py

# Falls welche fehlen → erstelle sie oder kopiere
```

---

## 🔧 CREATE .SKILL FILE

### Schritt 2: ZIP-Datei erstellen (macOS/Linux)

```bash
# Navigiere zum Projekt-Verzeichnis
cd ~/stallwache
# oder
cd /path/to/Stallwache

# Erstelle die .skill-Datei (ZIP-Archive mit speziellem Namen)
zip -r stallwache-v1.0.0.skill \
  SKILL.md \
  evals.json \
  README.md \
  README_FOR_GITHUB.md \
  CONTRIBUTING.md \
  CHANGELOG.md \
  LICENSE \
  requirements.txt \
  .env.example \
  main.py \
  config.py \
  stream_processor.py \
  detector.py \
  telegram_client.py \
  database.py \
  logger.py \
  metrics.py \
  Dockerfile \
  docker-compose.yml \
  deploy.sh \
  test_camera.py \
  health_check.sh \
  SETUP_ROLLEI.md \
  DEPLOY_NOW.md \
  QUICKSTART.md \
  USER_ONBOARDING_GUIDE.md \
  FAQ.md \
  GIT_INIT_STEPS.md

# Überprüfe Größe
ls -lh stallwache-v1.0.0.skill
```

**Unter Windows (PowerShell):**

```powershell
# Navigiere zum Verzeichnis
cd C:\Users\axe2k\Desktop\Projekt\ Stall\stallwache\Stallwache

# Methode 1: Mit Compress-Archive
Compress-Archive -Path SKILL.md, evals.json, README.md, CONTRIBUTING.md, `
  LICENSE, CHANGELOG.md, requirements.txt, .env.example, `
  main.py, config.py, stream_processor.py, detector.py, `
  telegram_client.py, database.py, logger.py, metrics.py, `
  Dockerfile, docker-compose.yml, test_camera.py, health_check.sh `
  -DestinationPath stallwache-v1.0.0.skill -Force

# Überprüfe Größe
(Get-Item stallwache-v1.0.0.skill).Length / 1MB
```

### Schritt 3: Validiere die .skill-Datei

```bash
# Überprüfe dass die Datei erstellt wurde
ls -lh stallwache-v1.0.0.skill

# Überprüfe Inhalt
unzip -l stallwache-v1.0.0.skill

# Überprüfe dass erforderliche Dateien enthalten sind
unzip -l stallwache-v1.0.0.skill | grep SKILL.md
unzip -l stallwache-v1.0.0.skill | grep evals.json
unzip -l stallwache-v1.0.0.skill | grep main.py
```

**Erwartet:**
```
Archive:  stallwache-v1.0.0.skill
  Length      Date    Time    Name
---------  ---------- -----   ----
    3500  05-10-2026 10:00   SKILL.md
     500  05-10-2026 10:00   evals.json
    2000  05-10-2026 10:00   README.md
     180  05-10-2026 10:00   main.py
   ...
---------                     -------
   ~50000                     XX files
```

### Schritt 4: Überprüfe Größe

```bash
# Größe prüfen
ls -lh stallwache-v1.0.0.skill

# Sollte sein: < 50 MB
# Typisch: 3-5 MB
```

---

## 🧪 TEST DER .SKILL-DATEI

### Schritt 5: Entpacke und überprüfe

```bash
# Erstelle Test-Verzeichnis
mkdir -p /tmp/skill-test
cd /tmp/skill-test

# Entpacke die .skill-Datei
unzip ~/stallwache/stallwache-v1.0.0.skill

# Überprüfe dass alles entpackt wurde
ls -la
```

**Erwartet:** Alle Dateien sind vorhanden

### Schritt 6: Prüfe wichtige Dateien

```bash
# Überprüfe SKILL.md
head -30 SKILL.md | grep -E "name:|description:"

# Überprüfe evals.json
cat evals.json | head -20

# Überprüfe LICENSE
head -5 LICENSE

# Überprüfe main.py
head -10 main.py
```

---

## 📝 MARKETPLACE SUBMISSION VORBEREITUNG

### Schritt 7: Marketplace-Metadaten vorbereiten

Speichere diese Informationen in einer Datei für die Submission:

```
SKILL NAME:
stallwache-v1.0.0

DISPLAY NAME:
🐄 Stallwache - AI Calf Birthing Detection

CATEGORY:
Agriculture / Livestock / Monitoring

TAGS:
cattle, ai, detection, monitoring, docker, yolov8, telegram, 
livestock, agriculture, automation, open-source

SHORT DESCRIPTION (< 100 chars):
AI-powered automatic calf birthing detection with Telegram alerts 
and 24/7 monitoring

LONG DESCRIPTION (< 500 words):
[See COWORK_MARKETPLACE_SUBMISSION.md for full text]

WEBSITE/GITHUB:
https://github.com/YOUR_USERNAME/stallwache-skill

CREATOR EMAIL:
stallwache123@gmail.com

VERSION:
1.0.0

AUTHOR:
Stallwache Team

LICENSE:
MIT (Open Source)
```

### Schritt 8: Screenshots vorbereiten (Optional aber empfohlen)

Marketplaces zeigen gerne Screenshots. Erstelle diese Bilder (1200x800px):

1. **Feature Overview** - Zeige die DEPLOY_NOW.md Befehle
2. **Architecture** - System-Diagramm
3. **Results** - Erfolgreiche Deployment-Logs

Speichere als:
- `screenshot-1-features.png`
- `screenshot-2-architecture.png`
- `screenshot-3-results.png`
- `logo-256x256.png` (Optional)

---

## 🚀 MARKETPLACE SUBMISSION

### Schritt 9: Creator Account auf Cowork erstellen

1. **Öffne**: https://cowork.anthropic.com/marketplace
2. **Klick**: "Become a Creator" oder "Sign Up"
3. **Verifiziere** deine Email: stallwache123@gmail.com
4. **Fülle Creator-Profil aus:**
   - Display Name: (dein Name)
   - Email: stallwache123@gmail.com
   - Website: https://github.com/YOUR_USERNAME/stallwache-skill
   - Support Email: stallwache123@gmail.com

### Schritt 10: Skill hochladen

1. **Gehe zu**: Creator Dashboard
2. **Klick**: "New Skill" oder "Add Skill"
3. **Wähle**: "Upload .skill file"
4. **Klick**: "Choose File"
5. **Wähle**: `stallwache-v1.0.0.skill`
6. **Klick**: "Upload"
7. **Warte**: System validiert die Datei

### Schritt 11: Metadaten ausfüllen

**Skill Details:**
- Name: Stallwache
- Version: 1.0.0
- Category: Agriculture / Livestock / Monitoring
- Tags: (siehe oben)
- Short Description: (siehe oben)
- Long Description: (siehe COWORK_MARKETPLACE_SUBMISSION.md)

**Creator Contact:**
- Display Name: Your Name
- Support Email: stallwache123@gmail.com
- Website: https://github.com/YOUR_USERNAME/stallwache-skill

### Schritt 12: Screenshots hochladen

1. **Klick**: "Add Screenshot"
2. **Wähle**: screenshot-1-features.png (1200x800px)
3. **Wähle**: screenshot-2-architecture.png (1200x800px)
4. **Wähle**: screenshot-3-results.png (1200x800px)
5. **Optional - Logo**: logo-256x256.png

### Schritt 13: Review & Publish

1. **Überprüfe** dass alles korrekt ist
2. **Klick**: "Submit for Review"
3. **Warte**: 2-5 Arbeitstage für Marketplace-Review
4. **Genehmigung** erhalten
5. **🎉 LIVE** im Marketplace!

---

## ✅ VERIFICATION CHECKLIST

Vor der Submission überprüfe:

```bash
# 1. .skill-Datei existiert
ls -lh stallwache-v1.0.0.skill
# Größe: < 50 MB ✓

# 2. SKILL.md ist drin
unzip -l stallwache-v1.0.0.skill | grep SKILL.md
# 1 Eintrag ✓

# 3. evals.json ist drin
unzip -l stallwache-v1.0.0.skill | grep evals.json
# 1 Eintrag ✓

# 4. Python-Code ist drin
unzip -l stallwache-v1.0.0.skill | grep main.py
# 1 Eintrag ✓

# 5. Datei kann entpackt werden
unzip -t stallwache-v1.0.0.skill
# Archive is OK ✓

# 6. Keine sensitiven Daten
unzip -p stallwache-v1.0.0.skill | grep -i "password\|token\|secret"
# Nichts gefunden ✓
```

---

## 🆘 TROUBLESHOOTING

### Error: "zip: command not found" (Linux/Mac)

**Lösung:**
```bash
# Installiere zip
brew install zip  # macOS
sudo apt-get install zip  # Ubuntu/Debian
```

### Error: "No such file or directory"

**Lösung:** Stelle sicher dass du im richtigen Verzeichnis bist
```bash
pwd
# Sollte zeigen: /path/to/Stallwache
```

### Error: "File too large" (> 50 MB)

**Lösung:** Entferne große Dateien:
```bash
# Überprüfe welche Dateien groß sind
find . -size +10M

# Entferne diese vor ZIP
# Dann erstelle .skill-Datei neu
```

### Skill wird beim Upload abgelehnt

**Überprüfe:**
- [ ] SKILL.md existiert und hat min. 500 Zeilen
- [ ] evals.json existiert mit min. 3 Test-Cases
- [ ] License existiert (MIT)
- [ ] README.md existiert
- [ ] Keine Credentials in Dateien (außer .env.example)
- [ ] Dateigröße < 50 MB

---

## 📦 NACH DER SUBMISSION

### Live im Marketplace

Wenn deine Skill genehmigt wurde:

```bash
# 1. Teile den Link
https://cowork.anthropic.com/marketplace/stallwache

# 2. Teile auf Social Media
# Twitter/X, LinkedIn, GitHub, etc.

# 3. Updates machen
# - Bug Fixes
# - New Features
# - v1.1.0, v2.0.0, etc.
```

### Updates pushen

```bash
# 1. Code ändern/verbessern
# 2. SKILL.md updaten
# 3. CHANGELOG.md aktualisieren
# 4. Neue .skill-Datei erstellen
# 5. Zu Marketplace hochladen

# Der Marketplace verwaltet automatisch:
# - Version updates
# - User notifications
# - Download history
```

---

## 📞 HILFE

Wenn Probleme bei der Submission auftreten:

```
Email: stallwache123@gmail.com
Subject: [MARKETPLACE] Skill Submission Issue

Beschreibe:
- Welcher Schritt
- Was ist fehlgeschlagen
- Welche Fehlermeldung
- Screenshots falls relevant
```

---

**Glückwunsch!** Deine .skill-Datei ist bereit für den Marketplace! 🎉

**Nächster Schritt**: Marketplace Submission auf https://cowork.anthropic.com/marketplace
