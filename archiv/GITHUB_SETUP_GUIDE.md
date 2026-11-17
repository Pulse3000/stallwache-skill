# 🐙 GitHub Repository Setup - Stallwache Skill

Vollständige Anleitung zum Erstellen und Konfigurieren des GitHub-Repositories für Stallwache.

---

## 📋 Voraussetzungen

Bevor du anfängst, brauchst du:

- ✅ GitHub-Account (kostenlos auf https://github.com)
- ✅ Git installiert auf deinem Computer
- ✅ SSH-Key oder GitHub CLI konfiguriert (optional aber empfohlen)
- ✅ Alle Stallwache-Dateien lokal vorhanden

---

## 🚀 Schritt 1: GitHub Repository erstellen

### 1.1 Gehe zu GitHub

```
1. Öffne: https://github.com/new
2. Oder: GitHub Home → "New" Button (oben links)
```

### 1.2 Repository-Details ausfüllen

```
Repository name:        stallwache-skill
Description:            AI-powered calf birthing detection system
Visibility:             Public
Initialize with:        ✅ Add README.md
                        ✅ Add .gitignore (Python)
                        ✅ Choose license (MIT)
```

### 1.3 Repository erstellen

Klick "Create repository" ✅

**Gratulationen!** Dein Repository ist jetzt live auf:
```
https://github.com/YOUR_USERNAME/stallwache-skill
```

---

## 📂 Schritt 2: Lokale Git-Initialisierung

### 2.1 Clone das neue Repository

```bash
# Navigiere zu deinem lokalen Stallwache-Verzeichnis
cd /path/to/stallwache

# Clone dein GitHub-Repo (um .git-Verzeichnis zu bekommen)
git clone https://github.com/YOUR_USERNAME/stallwache-skill.git temp-clone
cd temp-clone
cp -r .git ../stallwache/
cd ../stallwache
rm -rf ../temp-clone
```

Oder (Alternative - Direkter Weg):

```bash
# Initialisiere Git in bestehendem Verzeichnis
cd /path/to/stallwache
git init

# Füge GitHub als Remote hinzu
git remote add origin https://github.com/YOUR_USERNAME/stallwache-skill.git

# Fetch die GitHub-Dateien (README.md, .gitignore, LICENSE)
git pull origin main
# Falls das nicht funktioniert:
git fetch origin
git reset --hard origin/main
```

---

## 📝 Schritt 3: .gitignore konfigurieren

Erstelle/aktualisiere `.gitignore`:

```bash
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.venv
.env

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Project specific
data/
logs/
models/
*.db
*.db-journal
.env.production  # ⚠️ NICHT COMMITTEN!
.env.local

# Docker
.dockerignore
docker-compose.override.yml

# Tests
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
```

---

## 📁 Schritt 4: Repository-Struktur aufbauen

### Empfohlene Struktur:

```
stallwache-skill/
│
├── .github/
│   ├── workflows/
│   │   ├── tests.yml (CI/CD Pipeline)
│   │   └── release.yml (Auto-Release)
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
│
├── docs/
│   ├── DEPLOYMENT.md
│   ├── API.md
│   └── ARCHITECTURE.md
│
├── src/ (oder direktes Verzeichnis)
│   ├── main.py
│   ├── config.py
│   ├── stream_processor.py
│   ├── detector.py
│   ├── telegram_client.py
│   ├── database.py
│   ├── logger.py
│   └── metrics.py
│
├── tests/
│   ├── test_detector.py
│   ├── test_database.py
│   └── conftest.py
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── config/
│   ├── .env.example
│   └── config-template.json
│
├── scripts/
│   ├── deploy.sh
│   ├── setup.sh
│   └── health_check.sh
│
├── README.md (GitHub-README.md umbenennen)
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE (MIT)
├── requirements.txt
├── SKILL.md (Die Skill-Dokumentation)
├── evals.json (Test-Cases)
└── .gitignore
```

### Erstelle die Ordner-Struktur lokal:

```bash
mkdir -p .github/workflows .github/ISSUE_TEMPLATE
mkdir -p docs
mkdir -p src
mkdir -p tests
mkdir -p docker
mkdir -p config
mkdir -p scripts
```

---

## 📄 Schritt 5: GitHub-README erstellen

Benenne um/erstelle `README.md` (dient als GitHub-Frontpage):

```bash
# Verwende den existierenden GitHub_README.md
cp GitHub_README.md README.md

# Oder aktualisiere die Details:
# - Ersetze "stallwache123@gmail.com" mit deiner Email
# - Aktualisiere GitHub-Links zu deinem Repo
```

---

## 🐙 Schritt 6: GitHub Features konfigurieren

### 6.1 Branch Protection Rules

```
GitHub Settings → Branches → Add rule

Branch name pattern: main

☑ Require pull request reviews before merging
☑ Require status checks to pass before merging
☑ Require branches to be up to date before merging
☑ Dismiss stale pull request approvals
☑ Require code review from code owners
```

### 6.2 Issue Templates

Erstelle `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug report
about: Report a bug to help us improve
title: "[BUG] "
labels: bug
---

## Describe the bug
A clear description of what the bug is.

## Steps to reproduce
1. ...
2. ...
3. ...

## Expected behavior
What you expected to happen.

## Actual behavior
What actually happened.

## Environment
- OS: [e.g. Ubuntu 22.04]
- Python version: [e.g. 3.10.4]
- Docker version: [e.g. 20.10.17]

## Logs
```
Paste error logs here
```

## Additional context
Add any other context about the problem.
```

Erstelle `.github/ISSUE_TEMPLATE/feature_request.md`:

```markdown
---
name: Feature request
about: Suggest a feature to improve Stallwache
title: "[FEATURE] "
labels: enhancement
---

## Is your feature request related to a problem?
Describe the problem.

## Describe the solution you'd like
How should the feature work?

## Describe alternatives you've considered
Other approaches?

## Additional context
Add any other context or examples.
```

---

## 🔄 Schritt 7: Git Staging & Commit

### 7.1 Check Status

```bash
git status
# Shows all new/modified files
```

### 7.2 Add Files to Staging

```bash
# Add all Python files
git add src/
git add tests/

# Add configuration
git add docker/
git add config/
git add scripts/

# Add documentation
git add SKILL.md
git add evals.json
git add docs/

# Add GitHub configs
git add .github/
git add .gitignore

# Check what will be committed
git status
```

### 7.3 Create First Commit

```bash
git commit -m "feat: Initial Stallwache Skill v1.0.0 release

- Production-ready AI calf detection system
- 8 Python modules with comprehensive error handling
- Docker deployment with health checks
- SQLite event logging and metrics
- Telegram integration for alerts
- 3.500+ lines of documentation
- 3 test scenarios with 14 assertions (100% passing)
- MIT License - Open Source"
```

---

## 🚀 Schritt 8: Push zu GitHub

### 8.1 Push zum Repository

```bash
# Push zum main branch
git push -u origin main

# Überprüfe dass alles hochgeladen wurde
git log --oneline
git remote -v
```

### 8.2 Überprüfe auf GitHub

```
Öffne: https://github.com/YOUR_USERNAME/stallwache-skill
Überprüfe: Alle Dateien sind sichtbar
```

---

## 📋 Schritt 9: Zusätzliche GitHub Features

### 9.1 Topics hinzufügen

GitHub Repo Settings → Topic:

```
cattle
ai
detection
monitoring
docker
yolov8
telegram
agriculture
livestock
open-source
```

### 9.2 GitHub Pages aktivieren (Optional)

```
Settings → Pages → Source: main branch → save
```

Erstelle `docs/index.md` für dokumentations-Website.

### 9.3 Releases erstellen

```bash
git tag -a v1.0.0 -m "Version 1.0.0 - Initial Production Release"
git push origin v1.0.0

# Oder auf GitHub unter "Releases" → "Create a new release"
```

---

## 🤖 Schritt 10: CI/CD mit GitHub Actions (Optional)

Erstelle `.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=src
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

---

## 📊 Schritt 11: Repository-Statistiken

Nach der ersten Commit, wird GitHub automatisch anzeigen:

```
Repository Insights:
├─ Code frequency
├─ Network graph
├─ Contributors
├─ Community standards
└─ Security
```

---

## 🔗 Schritt 12: Links & Badges aktualisieren

In `README.md` und `CONTRIBUTING.md`:

Ersetze alle generischen Links mit deinen:

```markdown
# Vorher:
https://github.com/stallwache/skill

# Nachher:
https://github.com/YOUR_USERNAME/stallwache-skill
```

---

## 📝 Schritt 13: Repository-Beschreibung

GitHub Settings → General:

```
Description:
AI-powered calf birthing detection system with YOLOv8, 
Docker deployment, and Telegram alerts. Production-ready 
with comprehensive documentation.

Website: (optional)

Topics: cattle, ai, detection, monitoring, docker
```

---

## ✅ Finale Checkliste

- [ ] Repository auf GitHub erstellt
- [ ] Git lokal konfiguriert
- [ ] .gitignore gesetzt
- [ ] README.md aktualisiert
- [ ] CONTRIBUTING.md vorhanden
- [ ] LICENSE hinzugefügt
- [ ] CHANGELOG.md vorhanden
- [ ] GitHub Issues Templates erstellt
- [ ] Branch protection rules konfiguriert
- [ ] Topics hinzugefügt
- [ ] Erste Commits gepusht
- [ ] Release v1.0.0 erstellt
- [ ] GitHub Actions (optional) konfiguriert
- [ ] Repository öffentlich gemacht
- [ ] Link in deinen Dokumenten aktualisiert

---

## 🎯 Häufige Befehle

### Tägliche Arbeit

```bash
# Überprüfe Status
git status

# Add & Commit
git add .
git commit -m "feat: your message"

# Push zu GitHub
git push origin main

# Pull Updates
git pull origin main

# Erstelle Feature Branch
git checkout -b feature/your-feature
git push -u origin feature/your-feature

# Merge ein
git checkout main
git pull origin main
git merge feature/your-feature
git push origin main
```

### Branching-Strategie

```
main          → Production-ready releases
develop       → Development branch
feature/*     → Feature branches
fix/*         → Bug fix branches
release/*     → Release candidates
```

---

## 📚 Nützliche GitHub-Links

- **Repository**: https://github.com/YOUR_USERNAME/stallwache-skill
- **Issues**: https://github.com/YOUR_USERNAME/stallwache-skill/issues
- **Pull Requests**: https://github.com/YOUR_USERNAME/stallwache-skill/pulls
- **Releases**: https://github.com/YOUR_USERNAME/stallwache-skill/releases
- **Settings**: https://github.com/YOUR_USERNAME/stallwache-skill/settings

---

## 🤝 Community-Setup

### Welcoming New Contributors

1. **GitHub Discussions aktivieren**
   - Settings → Features → Discussions

2. **GitHub Wiki (Optional)**
   - Für zusätzliche Dokumentation
   - Settings → Features → Wiki

3. **Sponsorship (Optional)**
   - Settings → Sponsor link
   - Falls du Unterstützung annehmen möchtest

---

## 🚀 Nächste Schritte nach Setup

1. ✅ Repository ist live
2. ✅ Dokumentation ist sichtbar
3. 👉 **Teile den Link**: Mit Freunden, Social Media, etc.
4. 👉 **Sammle Feedback**: Issues, Discussions
5. 👉 **Verwalte PRs**: Von Contributors
6. 👉 **Releases**: v1.1, v2.0, etc.

---

## 📞 Support

Wenn GitHub-Probleme auftauchen:

- GitHub Docs: https://docs.github.com
- GitHub Community: https://github.community
- Email: stallwache123@gmail.com

---

**Glückwunsch!** Dein GitHub-Repository für Stallwache ist jetzt live! 🎉

**Version**: 1.0.0 | **Datum**: Mai 2026 | **Status**: Ready to Share 🚀
