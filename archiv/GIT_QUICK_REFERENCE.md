# 🐙 Git Quick Reference - Stallwache

Schnelle Git-Befehle für Stallwache-Entwicklung.

---

## 🚀 Erste Einrichtung (Einmalig)

```bash
# Repository clonen
git clone https://github.com/YOUR_USERNAME/stallwache-skill.git
cd stallwache-skill

# Git konfigurieren (falls noch nicht gemacht)
git config --global user.name "Dein Name"
git config --global user.email "deine@email.com"

# SSH-Key hinzufügen (optional, für passwordlose Authentifizierung)
ssh-keygen -t ed25519 -C "deine@email.com"
cat ~/.ssh/id_ed25519.pub  # Kopiere diesen Output
# Paste unter GitHub Settings → SSH and GPG keys
```

---

## 📝 Alltägliche Befehle

### Status & Info

```bash
# Zeige Änderungen
git status

# Zeige detaillierte Änderungen
git diff

# Zeige Commit-Historie
git log --oneline

# Zeige aktuelle Branch
git branch

# Zeige alle Branches (lokal + remote)
git branch -a
```

### Änderungen speichern

```bash
# Single file hinzufügen
git add path/to/file.py

# Alle Änderungen hinzufügen
git add .

# Interaktiv auswählen (empfohlen)
git add -p
# 'y' = ja, 'n' = nein, 's' = split, 'q' = quit

# Commit mit aussagekräftiger Nachricht
git commit -m "feat: Kurze Beschreibung"

# Oder mit längerer Beschreibung
git commit -m "feat: Kurze Zusammenfassung

- Detaillierte Erklärung
- Weitere Punkte
- Etc."

# Amend letzten Commit (falls Fehler)
git commit --amend

# Push zu GitHub
git push origin main
```

---

## 🌿 Branch Management

### Feature entwickeln

```bash
# Erstelle Feature Branch
git checkout -b feature/new-feature-name

# oder
git switch -c feature/new-feature-name

# Arbeit auf Feature Branch
git add .
git commit -m "feat: implement new feature"
git push -u origin feature/new-feature-name

# Erstelle Pull Request auf GitHub
# (GitHub zeigt einen Link nach dem Push)
```

### Verschiedene Branches

```bash
# Wechsel zu anderem Branch
git checkout main
# oder
git switch main

# Lösche lokalen Branch
git branch -d feature/old-feature

# Lösche Remote Branch
git push origin --delete feature/old-feature

# Branch mit main updaten
git fetch origin
git rebase origin/main
# oder
git merge origin/main
```

---

## 🔄 Updates von GitHub

```bash
# Hole neueste Änderungen
git fetch origin

# Integre diese in deinen Branch
git merge origin/main

# oder alles in einem Schritt
git pull origin main

# Mit Rebase statt Merge
git pull --rebase origin main
```

---

## 📋 Commit-Message Konvention

Verwende dieses Format für bessere Lesbarkeit:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types:

- **feat**: Neue Feature
- **fix**: Bug-Fix
- **docs**: Dokumentation
- **style**: Code-Stil (keine Logik-Änderung)
- **refactor**: Code-Umstrukturierung
- **perf**: Performance-Improvement
- **test**: Test-Hinzufügung
- **ci**: CI/CD-Änderungen

### Beispiele:

```bash
# Einfach
git commit -m "feat: Add multi-camera support"

# Mit Scope
git commit -m "fix(detector): correct confidence threshold"

# Detailliert
git commit -m "feat(api): Add REST endpoint for alerts

Add new /alerts endpoint to get alert history.
- Query by date range
- Filter by camera
- Pagination support

Closes #123"
```

---

## 🔍 Debugging & Probleme

### Fehler beheben

```bash
# Sehe welche Datei Fehler verursacht
git diff HEAD~1 -- path/to/file.py

# Zeige Änderungen von spezifischem Autor
git log --author="Name"

# Zeige Änderungen an spezifischer Datei
git log -p -- path/to/file.py

# Finde welcher Commit einen Bug einführte
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Git wird commits testen...
```

### Änderungen rückgängig machen

```bash
# Unstage eine Datei
git reset path/to/file.py

# Verwerfe lokale Änderungen
git checkout -- path/to/file.py

# oder mit neuerer Syntax
git restore path/to/file.py

# Revert letzten Commit (erstelle neuen Commit der Änderungen rückgängig macht)
git revert HEAD

# Lösche letzten Commit (lokal)
git reset --hard HEAD~1

# ⚠️ NUR wenn noch nicht gepusht!
```

### Stash (temporär speichern)

```bash
# Speichere Änderungen temporär
git stash

# Liste gestashte Änderungen
git stash list

# Hole Änderungen zurück
git stash pop

# oder spezifisch
git stash apply stash@{0}

# Lösche Stash
git stash drop stash@{0}
```

---

## 🔐 Remote Management

```bash
# Zeige Remote-URLs
git remote -v

# Füge Remote hinzu
git remote add upstream https://github.com/original-owner/stallwache-skill.git

# Entferne Remote
git remote remove upstream

# Benenne Remote um
git remote rename origin github
```

---

## 📊 Historie & Analyse

```bash
# Zeige Commits mit Statistiken
git log --stat

# Zeige Commit-Graphik (visuell)
git log --graph --oneline --all

# Zeige wer welche Zeile geschrieben hat
git blame path/to/file.py

# Zeige Commits die Datei gelöscht/geändert haben
git log --follow path/to/file.py

# Vergleiche Branches
git diff main feature/new-feature
```

---

## 🚀 Releases & Tags

```bash
# Erstelle Tag
git tag -a v1.0.0 -m "Version 1.0.0 Release"

# Push Tags zu GitHub
git push origin v1.0.0

# oder alle Tags
git push origin --tags

# Zeige alle Tags
git tag -l

# Lösche lokalen Tag
git tag -d v1.0.0

# Lösche Remote Tag
git push origin --delete v1.0.0
```

---

## 🌐 GitHub CLI (Optional)

Falls du GitHub CLI (`gh`) installiert hast:

```bash
# Login zu GitHub
gh auth login

# Erstelle Repository von Command Line
gh repo create stallwache-skill --public

# Erstelle Pull Request
gh pr create --title "feat: my feature" --body "Description"

# Überprüfe PR Status
gh pr status

# Merge PR
gh pr merge <PR_NUMBER>

# Erstelle Issue
gh issue create --title "Bug: something" --body "Description"
```

---

## 🎯 Best Practices

### Commits

✅ **DO:**
- Kleine, fokussierte Commits
- Aussagekräftige Nachrichten
- Eine Feature pro Commit
- Häufig committen

❌ **DON'T:**
- Große Commits mit vielen Änderungen
- Vage Nachrichten ("fix bugs")
- Tests und Code vermischen
- Credentials committen

### Branches

✅ **DO:**
- Feature Branches für neue Features
- Descriptive Branch-Namen
- Pull Requests für Code Review
- Branches löschen nach Merge

❌ **DON'T:**
- Direkt auf main committen
- Alte Branches nicht löschen
- Force push ohne guten Grund

### Push

✅ **DO:**
- Testen vor dem Push
- Regelmäßig pushen
- Mit Team kommunizieren
- Dokumentation mitaktualisieren

❌ **DON'T:**
- Broken Code pushen
- Uncommitted Changes
- .env und Credentials
- Große Binärdateien

---

## 🔗 Nützliche Links

```
Git Docs:        https://git-scm.com/doc
GitHub Docs:     https://docs.github.com
GitHub CLI:      https://cli.github.com
Git Visualizer:  https://git-school.github.io/visualizing-git/
```

---

## 💾 Git Config Tipps

```bash
# Globale Konfiguration setzen
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Standardeditor setzen
git config --global core.editor "nano"  # oder vim, code, etc.

# Line endings konfigurieren
git config --global core.autocrlf true  # Windows

# Alias für häufige Befehle
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.log1 "log --oneline"
git config --global alias.diff-staged "diff --staged"

# Zeige alle Konfigurationen
git config --list
```

---

## 🆘 Hilfe

```bash
# Git-Hilfe
git help <command>

# Beispiele
git help commit
git help push
git help merge
```

---

## 🎓 Learning Resources

```
Git Interactive Tutorial:
  https://learngitbranching.js.org/

Git Cheat Sheet:
  https://github.github.com/training-kit/

Pro Git Book (kostenlos):
  https://git-scm.com/book/en/v2
```

---

**Mit diesen Befehlen bist du bereit für GitHub-Collaboration!** 🚀

Viel Erfolg! 🐄
