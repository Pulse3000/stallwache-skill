# 🚀 Git Initialization - Step-by-Step

Führe diese Schritte aus, um Stallwache mit Git zu initialisieren und zu GitHub zu pushen.

---

## 📋 VORBEREITUNG

### Schritt 0: GitHub Account & Git Installation

**Falls noch nicht vorhanden:**

1. **GitHub Account erstellen**
   - Öffne: https://github.com/signup
   - Username: (z.B. "dein-name")
   - Email: stallwache123@gmail.com
   - Password: (sicher!)

2. **Git installieren** (falls noch nicht vorhanden)
   - macOS: `brew install git`
   - Windows: https://git-scm.com/download/win
   - Linux: `sudo apt-get install git`

3. **Git konfigurieren**
   ```bash
   git config --global user.name "Dein Name"
   git config --global user.email "stallwache123@gmail.com"
   ```

---

## 🔧 GIT SETUP (LOKAL)

### Schritt 1: Navigiere zum Projekt-Verzeichnis

```bash
# Öffne Terminal/PowerShell
# Navigiere zu Stallwache-Verzeichnis

cd /path/to/Stallwache
# oder unter Windows:
cd C:\Users\axe2k\Desktop\Projekt\ Stall\stallwache\Stallwache

# Überprüfe dass du im richtigen Verzeichnis bist
pwd
ls -la  # oder "dir" unter Windows
```

**Du solltest sehen:**
```
SKILL.md
evals.json
README.md
main.py
config.py
...
```

### Schritt 2: Git Repository initialisieren

```bash
# Initialisiere Git
git init

# Überprüfe Status
git status
```

**Erwartet:**
```
fatal: Not a git repository yet
```

oder

```
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .gitignore
        SKILL.md
        evals.json
        ...
```

### Schritt 3: Git Benutzer konfigurieren (Lokal)

```bash
# Konfiguriere user.name & user.email FÜR DIESES REPO
git config user.name "Dein Name"
git config user.email "stallwache123@gmail.com"

# Überprüfe
git config user.name
git config user.email
```

### Schritt 4: Alle Dateien hinzufügen

```bash
# Überprüfe Status
git status

# Addiere alle Dateien
git add .

# Überprüfe was hinzugefügt wurde
git status
```

**Erwartet:**
```
On branch master

No commits yet

Changes to be committed:
  new file:   .gitignore
  new file:   SKILL.md
  new file:   evals.json
  ...
```

### Schritt 5: Ersten Commit erstellen

```bash
# Erstelle einen aussagekräftigen Commit-Message
git commit -m "feat: Initial Stallwache v1.0.0 production release

- Production-ready AI calf birthing detection system
- 8 Python modules with comprehensive error handling (~1.160 lines)
- Real-time YOLOv8 object detection (28-30 FPS @ 1080p)
- Telegram integration with image alerts
- SQLite event logging with 30-day auto-cleanup
- Docker containerization with health checks and auto-restart
- DDNS integration for remote access
- Comprehensive documentation (3.500+ lines SKILL.md)
- Complete test suite (3 scenarios, 14 assertions - 100% passing)
- MIT License - Open Source
- Rollei Safetycam HD 20 integration verified
- Multi-level user documentation (Quick/Standard/Expert)"

# Überprüfe commit
git log --oneline
```

**Erwartet:**
```
a1b2c3d (HEAD -> master) feat: Initial Stallwache v1.0.0 production release
```

---

## 🐙 GITHUB SETUP

### Schritt 6: GitHub Repository erstellen

1. **Öffne GitHub**
   - Gehe zu: https://github.com/new

2. **Fülle Formular aus:**

   ```
   Repository name:        stallwache-skill
   Description:            AI-powered calf birthing detection system
   
   Visibility:             ☑ Public
   
   Initialize this repository with:
                           ☑ Add a README file
                           ☑ Add .gitignore (Python)
                           ☑ Choose a license (MIT)
   ```

3. **Klick "Create repository"**

4. **Kopiere die Repository-URL**
   - Sollte sein: `https://github.com/YOUR_USERNAME/stallwache-skill.git`

### Schritt 7: GitHub als Remote hinzufügen

```bash
# Füge GitHub als Remote hinzu
# Ersetze YOUR_USERNAME mit deinem GitHub-Benutzernamen!
git remote add origin https://github.com/YOUR_USERNAME/stallwache-skill.git

# Überprüfe dass Remote hinzugefügt wurde
git remote -v
```

**Erwartet:**
```
origin  https://github.com/YOUR_USERNAME/stallwache-skill.git (fetch)
origin  https://github.com/YOUR_USERNAME/stallwache-skill.git (push)
```

### Schritt 8: Branch in "main" umbenennen (falls nötig)

```bash
# Moderne GitHub verwendet "main" statt "master"
git branch -M main

# Überprüfe current branch
git branch
```

**Erwartet:**
```
* main
```

### Schritt 9: Zu GitHub pushen

```bash
# Push zum main branch auf GitHub
git push -u origin main

# Das "-u" bedeutet: setze upstream tracking
# Die nächsten pushes funktionieren dann mit nur "git push"
```

**Erwartet:**
```
Enumerating objects: 50, done.
Counting objects: 100% (50/50), done.
Delta compression using up to 8 threads
Compressing objects: 100% (40/40), done.
Writing objects: 100% (50/50), ...
...
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

### Schritt 10: Überprüfe auf GitHub

1. **Öffne**: https://github.com/YOUR_USERNAME/stallwache-skill
2. **Überprüfe dass:**
   - [ ] README.md ist sichtbar
   - [ ] Alle Python-Dateien sind sichtbar
   - [ ] SKILL.md ist sichtbar
   - [ ] evals.json ist sichtbar
   - [ ] LICENSE ist sichtbar
   - [ ] .gitignore ist vorhanden (verborgen, aber existiert)

---

## 🔄 GITHUB FEATURES KONFIGURIEREN

### Schritt 11: Branch Protection konfigurieren

1. **Gehe zu Settings → Branches**
   - URL: https://github.com/YOUR_USERNAME/stallwache-skill/settings/branches

2. **Klick "Add rule"**

3. **Konfiguriere:**
   ```
   Branch name pattern: main
   
   ☑ Require pull request reviews before merging
   ☑ Require status checks to pass before merging
   ☑ Require branches to be up to date before merging
   ☑ Dismiss stale pull request approvals
   ```

4. **Klick "Create"**

### Schritt 12: Topics hinzufügen

1. **Gehe zu Settings → General**
   - URL: https://github.com/YOUR_USERNAME/stallwache-skill/settings

2. **Scrolle zu "Topics"**

3. **Füge folgende Topics hinzu:**
   ```
   cattle, ai, detection, monitoring, docker, yolov8, 
   agriculture, livestock, open-source, automation
   ```

### Schritt 13: GitHub Actions aktivieren

GitHub Actions sollten automatisch aktiviert sein, aber überprüfe:

1. **Gehe zu Actions**
   - URL: https://github.com/YOUR_USERNAME/stallwache-skill/actions

2. **Überprüfe dass "Tests" workflow existiert**
   - Falls ja: ✅ Perfect!
   - Falls nein: Manuell die Datei hochladen

### Schritt 14: Release erstellen (Optional aber empfohlen)

```bash
# Erstelle einen Tag
git tag -a v1.0.0 -m "Stallwache v1.0.0 - Production Ready"

# Push Tag zu GitHub
git push origin v1.0.0
```

Oder auf GitHub selbst:
1. **Gehe zu Releases** → https://github.com/YOUR_USERNAME/stallwache-skill/releases
2. **Klick "Create a new release"**
3. **Fülle aus:**
   - Tag: v1.0.0
   - Title: Stallwache v1.0.0 - Production Ready
   - Description: (kopiere aus RELEASE_NOTES_TEMPLATE.md)

---

## ✅ VERIFICATION CHECKLIST

```bash
# 1. Überprüfe git status
git status
# Sollte zeigen: "On branch main, nothing to commit"

# 2. Überprüfe git log
git log --oneline -5
# Sollte deine Commits zeigen

# 3. Überprüfe remote
git remote -v
# Sollte zeigen: origin https://github.com/YOUR_USERNAME/stallwache-skill.git

# 4. Überprüfe branch
git branch
# Sollte zeigen: * main

# 5. Überprüfe dass Dateien auf GitHub sind
# Öffne https://github.com/YOUR_USERNAME/stallwache-skill
# Überprüfe dass Dateien sichtbar sind
```

---

## 🚀 NÄCHSTE SCHRITTE

Nach erfolgreichem GitHub Push:

1. **Erstelle .skill-Datei**
   ```bash
   zip -r stallwache-v1.0.0.skill SKILL.md evals.json ...
   ```

2. **Submitta zu Marketplace**
   - https://cowork.anthropic.com/marketplace
   - Creator Account
   - Upload .skill file

3. **Teile dein Repository**
   - GitHub Link teilen
   - Social Media
   - Netzwerk

---

## 🆘 TROUBLESHOOTING

### Error: "fatal: origin does not appear to be a git repository"

**Lösung:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/stallwache-skill.git
```

### Error: "Permission denied (publickey)"

**Lösung:** Verwende HTTPS statt SSH
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/stallwache-skill.git
```

### Error: "fatal: pathspec ... did not match"

**Lösung:** Überprüfe dass du im richtigen Verzeichnis bist
```bash
pwd
git status
```

### Dateien werden nicht gepusht

**Lösung:** Überprüfe dass sie geadded & committed sind
```bash
git add .
git commit -m "message"
git push origin main
```

---

## 📞 HILFE BRAUCHEN?

- **Git Docs**: https://git-scm.com/docs
- **GitHub Docs**: https://docs.github.com
- **Email**: stallwache123@gmail.com

---

**Du schaffst das!** 🐄🚀

Sobald GitHub setup ist → Weiter zu NEXT_STEPS.md für Schritt 2 (Marketplace Submission)
