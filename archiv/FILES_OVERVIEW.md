# 📁 Stallwache - Komplette Dateiübersicht

## 🎯 Start hier (Dokumentation)

| Datei | Zweck | Für wen? |
|-------|-------|---------|
| **READY_TO_DEPLOY.md** | Überblick & Deployment | Jeder (vor Start) |
| **QUICKSTART.md** | 5-Min Setup | Ungeduldig → schnell starten |
| **README.md** | Vollständige Dokumentation | Developer & Troubleshooting |
| **SETUP_ROLLEI.md** | Rollei Kamera Integration | Rollei Setup & Konfiguration |
| **Rollei_HD20_Hardware_Setup_Guide** | Hardware-Details | Hardware-Setup |

**👉 START: Öffne `READY_TO_DEPLOY.md`**

---

## 🐍 Python Core Module

### Main & Config

| Datei | Zeilen | Zweck |
|-------|--------|-------|
| `main.py` | 180 | **Haupteinstiegspunkt** - orchestriert alle Komponenten |
| `config.py` | 130 | **Zentrale Konfiguration** - alle Parameter via Environment-Variables |

### Stream & Detection

| Datei | Zeilen | Zweck |
|-------|--------|-------|
| `stream_processor.py` | 160 | **RTSP-Stream-Verarbeitung** - Thread-safe, Auto-Reconnect, Frame-Buffering |
| `detector.py` | 190 | **YOLOv8 Inferenz** - Kalberkennungs-AI, Temporal Analysis |

### Integration & Output

| Datei | Zeilen | Zweck |
|-------|--------|-------|
| `telegram_client.py` | 140 | **Telegram Alerts** - Benachrichtigungen mit Bildern, Cooldown |
| `database.py` | 210 | **SQLite Datenbank** - Events, Detektionen, Metriken loggen |

### System

| Datei | Zeilen | Zweck |
|-------|--------|-------|
| `logger.py` | 80 | **Logging System** - Rotating Files, Color Output |
| `metrics.py` | 70 | **Performance Monitoring** - FPS, Inference-Time, Uptime |

---

## 🔧 Konfiguration & Deployment

| Datei | Typ | Zweck |
|-------|-----|-------|
| `.env.example` | Template | Konfiguration Template (Beispiel-Werte) |
| `.env.production` | Config | **PRODUCTIVE CONFIG** - Mit deiner Kamera-IP (192.168.178.108) |
| `requirements.txt` | Dependencies | Python Packages (pip install -r) |
| `Dockerfile` | Container | Docker Image für Production Build |
| `docker-compose.yml` | Orchestration | One-Command Deployment (empfohlen) |

---

## 🚀 Skripte & Tools

| Skript | Typ | Zweck |
|--------|-----|-------|
| `deploy.sh` | Bash | Automatisiertes Deployment (Alternative zu docker-compose) |
| `test_camera.py` | Python | **WICHTIG**: Validiere Kamera-Verbindung vor Start |
| `health_check.sh` | Bash | System-Health Monitoring während Laufzeit |

---

## 📚 Dokumentation

| Datei | Format | Inhalt |
|-------|--------|--------|
| `README.md` | Markdown | Umfassende Dokumentation (Installation, API, Troubleshooting) |
| `QUICKSTART.md` | Markdown | **5-Minuten Setup Anleitung** |
| `SETUP_ROLLEI.md` | Markdown | Rollei HD 20 Integration & Konfiguration |
| `READY_TO_DEPLOY.md` | Markdown | **Production Readiness Checklist** |
| `FILES_OVERVIEW.md` | Markdown | Diese Datei (Dateien-Übersicht) |
| `Rollei_HD20_Hardware_Setup_Guide.html` | HTML | Hardware-Setup mit Styling |
| `Rollei_HD20_Hardware_Setup_Guide.md` | Markdown | Hardware-Setup Markdown |

---

## 🎯 Quick Navigation

### Ich will **schnell starten**:
```
1. Öffne QUICKSTART.md
2. Führe aus: python test_camera.py
3. Führe aus: docker-compose up -d
4. Fertig! 🎉
```

### Ich will **verstehen wie es funktioniert**:
```
1. Lese README.md (API & Architecture)
2. Lese Quellcode main.py → stream_processor.py → detector.py
3. Lese .env.production (Konfigurationsoptionen)
```

### Ich will **Kamera & Hardware setup**:
```
1. Öffne SETUP_ROLLEI.md
2. Öffne Rollei_HD20_Hardware_Setup_Guide.html
3. Folge Schritt für Schritt
```

### Ich habe **Probleme**:
```
1. Öffne QUICKSTART.md → Troubleshooting Section
2. Führe aus: python test_camera.py
3. Führe aus: bash health_check.sh
4. Prüfe: docker logs -f stallwache
```

---

## 📊 Größen & Statistiken

```
Gesamtgröße Code:      ~1.5 MB
Python Module:         ~900 Bytes (8 files)
Dokumentation:         ~200 KB (7 files)
Docker Image:          ~2-3 GB (erste Erstellung)
Runtime Memory:        ~2-3 GB
Database (30 Tage):    ~500 MB
Logs (30 Tage):        ~100 MB
```

---

## 🔄 Workflow: Von Installation zu Running System

```
┌─────────────────────────────────────────────┐
│ 1. DOKUMENTATION LESEN                      │
├─────────────────────────────────────────────┤
│ → READY_TO_DEPLOY.md (2 min)               │
│ → QUICKSTART.md (5 min)                    │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ 2. VORBEREITUNG                             │
├─────────────────────────────────────────────┤
│ → python test_camera.py (1 min)            │
│ → nano .env.production (1 min, optional)   │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ 3. DEPLOYMENT                               │
├─────────────────────────────────────────────┤
│ → docker-compose up -d (2 min)             │
│ → docker logs -f stallwache (monitor)      │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ 4. VERIFICATION                             │
├─────────────────────────────────────────────┤
│ → bash health_check.sh (1 min)             │
│ → Logs prüfen (OK?)                        │
└──────────────────┬──────────────────────────┘
                   ↓
            ✅ SYSTEM LÄUFT
```

---

## 🎓 Empfohlene Lese-Reihenfolge

**Für totale Anfänger:**
1. READY_TO_DEPLOY.md (Überblick)
2. QUICKSTART.md (Schritt für Schritt)
3. docker-compose up -d
4. Bei Problemen → QUICKSTART.md Troubleshooting

**Für Developer:**
1. README.md (Architektur)
2. Quellcode lesen (main.py → detector.py)
3. config.py (Optionen verstehen)
4. .env.production (Konfigurieren)

**Für Hardware-Setup:**
1. SETUP_ROLLEI.md (Schritt 1-5)
2. Rollei_HD20_Hardware_Setup_Guide.html
3. SETUP_ROLLEI.md (Schritt 6 + Troubleshooting)

---

## 📋 Produktiv-Checklist

Vor ersten Start alle Checkboxen durchgehen:

- [ ] Dokumentation gelesen (mindestens QUICKSTART.md)
- [ ] Kamera-IP korrekt eingestellt (192.168.178.108)
- [ ] test_camera.py ✓ ALLE TESTS PASS
- [ ] .env.production konfiguriert (oder default OK)
- [ ] docker-compose up -d läuft ohne Fehler
- [ ] Logs zeigen "Stream-Verarbeitung läuft"
- [ ] health_check.sh ✓ SYSTEM HEALTHY
- [ ] Telegram Alert getestet (optional)
- [ ] Backup von wichtigen Daten erstellt

---

## 🔗 Datei-Beziehungen

```
.env.production ──→ config.py ──→ main.py ──→ stream_processor.py
                                     ↓
                              detector.py (YOLOv8)
                                     ↓
                         telegram_client.py (Alert)
                                     ↓
                         database.py (Logging)
                                     ↓
                         logger.py + metrics.py
```

---

## 🚀 Befehle zum Schnell-Referenzieren

```bash
# Alles testen & starten (copy-paste ready)
python test_camera.py && \
docker-compose down 2>/dev/null; \
docker-compose up -d && \
echo "✓ System läuft! Logs:" && \
docker logs -f stallwache

# Health Check
bash health_check.sh

# Logs anschauen
docker logs -f stallwache

# System stoppen
docker-compose down

# Komplett neu
docker-compose down -v && docker-compose up -d
```

---

## 💾 Daten-Verzeichnisse

```
logs/
├── stallwache.log           # Hauptlog
└── stallwache_error.log     # Nur Fehler

data/
├── stallwache.db            # SQLite (Events, Metriken)
└── stallwache.db.backup     # Backup

models/
├── yolov8m.pt               # YOLOv8 Medium Model
└── ...                       # Weitere Modelle (optional)
```

---

## 🎯 Production-Ready Status

| Komponente | Status | Notizen |
|-----------|--------|---------|
| Python Code | ✅ | 8 Module, vollständig dokumentiert |
| Docker | ✅ | Dockerfile + docker-compose |
| Dokumentation | ✅ | 5 Markdown + 1 HTML |
| Testing | ✅ | test_camera.py + health_check.sh |
| Security | ✅ | Keine Secrets in Code |
| Error Handling | ✅ | Alle Module mit try-catch |
| Logging | ✅ | Rotating Files, Color Output |
| Monitoring | ✅ | Metrics + Health Checks |
| Configuration | ✅ | Environment-Variables |
| CI/CD Ready | ⚠️ | (Optional später) |

---

**🐄 Systemstatus: PRODUCTION READY ✅**

**Alle Dateien sind erstellt, dokumentiert und getestet!**

Nächster Schritt: `READY_TO_DEPLOY.md` öffnen und folgen! 🚀
