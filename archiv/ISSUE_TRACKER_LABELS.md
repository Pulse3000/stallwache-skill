# GitHub Issue Labels Setup

Diese Datei enthält die empfohlenen Labels für das GitHub-Repository.

---

## 🏷️ Label-Kategorien & Farben

### 🐛 Bug-Labels

```
bug
  Color: #d73a49 (Red)
  Description: Something isn't working

critical
  Color: #b60205 (Dark Red)
  Description: Critical issue - needs immediate attention

regression
  Color: #e99695 (Light Red)
  Description: Bug that worked in a previous version
```

### ✨ Feature-Labels

```
enhancement
  Color: #a2eeef (Light Blue)
  Description: New feature or request

feature-request
  Color: #d4c5f9 (Light Purple)
  Description: Feature request from community

roadmap
  Color: #0075ca (Blue)
  Description: Part of the product roadmap
```

### 📖 Documentation

```
documentation
  Color: #0075ca (Blue)
  Description: Improvements or additions to documentation

good-first-issue
  Color: #7057ff (Purple)
  Description: Good for newcomers to the project

help-wanted
  Color: #008672 (Green)
  Description: Extra attention is needed
```

### 🔧 Maintenance

```
refactor
  Color: #fbca04 (Yellow)
  Description: Code refactoring without behavior change

tech-debt
  Color: #d4af37 (Gold)
  Description: Technical debt that should be addressed

performance
  Color: #006b75 (Teal)
  Description: Performance improvement

dependencies
  Color: #0366d6 (Dark Blue)
  Description: Dependencies update
```

### 🎯 Priority

```
p0-critical
  Color: #b60205 (Dark Red)
  Description: Critical - Fix immediately

p1-high
  Color: #d73a49 (Red)
  Description: High priority

p2-medium
  Color: #fbca04 (Yellow)
  Description: Medium priority

p3-low
  Color: #dddddd (Light Gray)
  Description: Low priority - Can wait
```

### 📋 Status

```
blocked
  Color: #e8ebf0 (Gray)
  Description: Blocked by another issue/PR

in-progress
  Color: #cccccc (Medium Gray)
  Description: Currently being worked on

needs-review
  Color: #fbca04 (Yellow)
  Description: Needs code or design review

needs-design
  Color: #cccccc (Medium Gray)
  Description: Needs design discussion

waiting-for-feedback
  Color: #cccccc (Medium Gray)
  Description: Waiting for user/contributor feedback

won't-fix
  Color: #ffffff (White)
  Description: Decision made not to fix

duplicate
  Color: #cfd3d7 (Light Gray)
  Description: Duplicate of another issue
```

### 🚀 Release

```
for-next-release
  Color: #0075ca (Blue)
  Description: Candidate for next release

release
  Color: #27d100 (Green)
  Description: Release-related task
```

### 🎪 Community

```
community
  Color: #ffd700 (Gold)
  Description: Community contributed

question
  Color: #d876e3 (Purple)
  Description: Further information is requested

discussion
  Color: #76daea (Cyan)
  Description: Discussion topic
```

---

## 🛠️ Wie man Labels hinzufügt

### Auf GitHub

1. Gehe zu: Repository → Issues → Labels
2. Klick "New label"
3. Fülle Name, Farbe, Beschreibung aus
4. Klick "Create label"

### Automatisiert (GitHub API)

```bash
#!/bin/bash

# Labels automatisch erstellen
curl -X POST https://api.github.com/repos/YOUR_USERNAME/stallwache-skill/labels \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -d '{"name":"bug","color":"d73a49","description":"Something is not working"}'
```

---

## 📋 Nutzungs-Richtlinien

### Issue-Labeling

Jedes Issue sollte haben:

1. **Genau ein** Type-Label (bug, enhancement, documentation, etc.)
2. **Optional ein** Priority-Label (p0-critical, p1-high, etc.)
3. **Optional ein** Status-Label (blocked, in-progress, etc.)
4. **Optional weitere** Labels (dependencies, community, etc.)

### Beispiele

```
Bug Issue:
  [bug] [p1-high] [needs-review]

Feature Request:
  [enhancement] [roadmap] [good-first-issue]

Documentation:
  [documentation] [help-wanted]

Performance:
  [performance] [p2-medium] [in-progress]
```

---

## 🔄 Label-Verwaltung

### Automatische Label-Zuordnung (GitHub Actions)

```yaml
name: Auto-label Issues

on:
  issues:
    types: [opened]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: github/issue-labeler@v2.4
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          configuration-path: .github/labeler.yml
          enable-versioned-regex: false
          delete-labeler-branch: false
```

### Archiviere alte Issues

Nutze GitHub's automatische Archivierung:
- Settings → General → Inactivity period for issue/PR stale
- Set to: 90 days
- Stale label: `stale`

---

## 📊 Auswertungen

Mit korrekten Labels kannst du:

- **Dashboards erstellen**: Filterung nach Labels
- **Milestones planen**: Issues pro Release gruppieren
- **Reports generieren**: Progress tracking
- **Community helfen**: Mit `good-first-issue` neue Contributors finden

---

## 🎯 Best Practices

✅ **DO:**
- Labels sparsam verwenden (5-8 pro Issue)
- Konsistent labeln
- Labels bei Änderungen aktualisieren
- Team auf Label-Konventionen einigen

❌ **DON'T:**
- Zu viele Labels pro Issue
- Labels nicht pflegen
- Veraltete Labels verwenden
- Labels auf vage Namen geben

---

**Diese Labels helfen dir und deinen Contributors, GitHub effektiv zu nutzen!** 🎯
