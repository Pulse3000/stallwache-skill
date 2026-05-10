# 🚀 Stallwache Vercel Deployment - Complete Guide

Deploy Stallwache zu Vercel für cloud-basierte Überwachung und REST API Zugriff.

---

## 📋 Prerequisites

- ✅ GitHub Repository erstellt (`stallwache-skill`)
- ✅ Alle Code-Dateien zu GitHub gepusht
- ✅ Vercel Account (kostenlos auf https://vercel.com)
- ✅ Git auf dem Computer konfiguriert
- ✅ Python 3.10+

---

## 🎯 Was Du mit Vercel bekommst

```
✓ Cloud Hosting (serverless functions)
✓ REST API Endpoints für remote Zugriff
✓ Real-time Monitoring Dashboard
✓ Auto-Scaling auf Demand
✓ Custom Domain Support
✓ Environment Variable Management
✓ Automatische Deployments bei git push
✓ Kostenlos Tier verfügbar
✓ Deployed in <3 Minuten
```

---

## 🔧 Phase 1: Vorbereitung - GitHub Repository Update

### 1.1 Neue Dateien zur Vorbereitung

Folgende Dateien wurden erstellt für Vercel-Kompatibilität:

```
✅ vercel_app.py     - Serverless Handler (REST API)
✅ api/handler.py    - Vercel API Route Handler
✅ vercel.json       - Vercel Konfiguration
✅ test_vercel_api.py - Lokale API Tests
```

### 1.2 Push zu GitHub

```bash
# Navigate to project
cd C:\Users\axe2k\Desktop\Projekt\ Stall\stallwache\Stallwache

# Add new files
git add vercel_app.py api/handler.py vercel.json test_vercel_api.py

# Commit
git commit -m "feat: Add Vercel serverless deployment configuration"

# Push
git push origin main
```

**Oder verwende dein auto_deploy.ps1 Script:**
```powershell
.\auto_deploy.ps1
```

---

## 🌐 Phase 2: Vercel Deployment

### 2.1 Vercel Account erstellen

1. Öffne: https://vercel.com
2. Melde Dich mit GitHub an
3. Autorisiere Vercel, auf Deine GitHub Repos zuzugreifen

### 2.2 GitHub Repository importieren

1. Dashboard → "Add New..." → "Project"
2. Wähle Dein GitHub Account
3. Finde und wähle: `stallwache-skill`
4. Klicke "Import"

### 2.3 Configure Environment Variables

Vercel wird Dich fragen nach Environment Variables. Füge diese hinzu:

```
CAMERA_RTSP_URL=rtsp://admin:PASSWORD@192.168.178.108/stream
CAMERA_USERNAME=admin
CAMERA_PASSWORD=YOUR_CAMERA_PASSWORD
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_CHAT_ID
ENABLE_TELEGRAM=true
DEVICE=cpu
YOLO_MODEL_PATH=./models/yolov8m.pt
CONFIDENCE_THRESHOLD=0.65
FRAME_SKIP=1
LOG_LEVEL=INFO
LOG_RETENTION_DAYS=30
ENVIRONMENT=production
```

**Wichtig:**
- Ersetze `PASSWORD` mit Deinem Camera-Passwort
- Ersetze `YOUR_BOT_TOKEN` mit Deinem Telegram Bot Token
- Ersetze `YOUR_CHAT_ID` mit Deiner Telegram Chat ID

### 2.4 Deploy

1. Klicke "Deploy"
2. Warte auf Deployment-Abschluss (1-3 Minuten)
3. Du bekommst eine URL wie: `https://stallwache-skill.vercel.app`

---

## 🌍 Phase 3: Dein Deployment testen

### 3.1 Besuche Dein Deployment

Gehe zu: `https://stallwache-skill.vercel.app`

Du solltest sehen:
```json
{
  "name": "Stallwache",
  "version": "1.0.0",
  "deployment": "vercel-serverless",
  "status": "running",
  "endpoints": {
    "health": "/api/health",
    "status": "/api/status",
    "events": "/api/events?hours=24",
    "statistics": "/api/statistics?days=30",
    "config": "/api/config"
  },
  "documentation": "https://github.com/stallwache/skill"
}
```

### 3.2 Test alle API Endpoints

**Health Check:**
```
https://stallwache-skill.vercel.app/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-05-10T12:34:56.789123",
  "uptime_seconds": 3456,
  "version": "1.0.0-vercel",
  "camera": "configured",
  "api": "REST v1"
}
```

---

**Current Status:**
```
https://stallwache-skill.vercel.app/api/status
```

**Response:**
```json
{
  "status": "running",
  "timestamp": "2026-05-10T12:34:56.789123",
  "system": {
    "version": "1.0.0",
    "deployment": "vercel",
    "environment": "production",
    "region": "iad1"
  },
  "camera": {
    "configured": true,
    "protocol": "RTSP"
  },
  "detection": {
    "model": "yolov8m.pt",
    "confidence_threshold": 0.65,
    "device": "cpu",
    "frame_skip": 1
  },
  "messaging": {
    "telegram_enabled": true,
    "configured": true
  },
  "database": {
    "type": "sqlite",
    "retention_days": 30
  }
}
```

---

**Events (last 24 hours):**
```
https://stallwache-skill.vercel.app/api/events?hours=24
```

**Events (last 48 hours):**
```
https://stallwache-skill.vercel.app/api/events?hours=48
```

---

**Statistics (last 30 days):**
```
https://stallwache-skill.vercel.app/api/statistics?days=30
```

**Statistics (last 90 days):**
```
https://stallwache-skill.vercel.app/api/statistics?days=90
```

---

**Configuration (ohne Secrets):**
```
https://stallwache-skill.vercel.app/api/config
```

---

## 🔐 Phase 4: Dein Deployment sichern

### 4.1 Custom Domain (Optional)

1. Vercel Dashboard → Project Settings → Domains
2. Füge Deine Domain hinzu oder verwende Vercel's Subdomain
3. Konfiguriere DNS wenn nötig

### 4.2 API Key Authentication (Optional)

Für Production: Füge API Key Authentication hinzu

```bash
# In vercel.json
"env": {
  "API_KEY": "@api_key_secret"
}
```

Dann verwende in Requests:
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://stallwache-skill.vercel.app/api/status
```

### 4.3 CORS Configuration (für Web-Frontend)

Falls Du ein Web-Frontend hast, konfiguriere CORS:

```python
# In vercel_app.py handler()
headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",  # oder spezifische Domain
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
}
```

---

## 📊 Phase 5: Monitoring & Observability

### 5.1 Vercel Dashboard Monitoring

1. Gehe zu: https://vercel.com/dashboard
2. Wähle: `stallwache-skill` Projekt
3. Schaue Dir an:
   - Deployment History
   - Build Logs
   - Performance Metrics
   - Runtime Errors

### 5.2 Real-Time Logs anschauen

```bash
# Install Vercel CLI
npm install -g vercel

# View logs in real-time
vercel logs stallwache-skill --follow

# View logs with filter
vercel logs stallwache-skill --until 1h
```

### 5.3 Health Monitoring Script

Erstelle ein lokales Monitoring-Script:

```bash
#!/bin/bash
# monitor_stallwache.sh - Health Check alle 5 Minuten

ENDPOINT="https://stallwache-skill.vercel.app/api/health"

while true; do
    RESPONSE=$(curl -s $ENDPOINT)
    STATUS=$(echo $RESPONSE | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    
    if [ "$STATUS" = "healthy" ]; then
        echo "✓ $(date): Stallwache is healthy"
    else
        echo "✗ $(date): Stallwache is unhealthy!"
        # Send alert here
    fi
    
    sleep 300  # 5 minutes
done
```

---

## 🔄 Phase 6: Automatische Deployments

### 6.1 Git Integration

Jedes Mal wenn Du zu GitHub pushst:

```bash
git add .
git commit -m "fix: Improve detection accuracy"
git push origin main
```

Vercel macht automatisch:
1. Detektiert den Change
2. Builds das Projekt
3. Deployed zur Production
4. Updated Deine API

### 6.2 Preview Deployments

Push zu einem neuen Branch für Preview-URL:

```bash
git checkout -b feature/new-detection-model
git push origin feature/new-detection-model
```

Vercel erstellt automatisch eine Preview-URL zum Testen vor dem Merge.

### 6.3 Rollback bei Fehler

Falls Dein Deployment fehlschlägt:

1. Vercel Dashboard → Deployments
2. Klicke auf den letzten erfolgreichen Deployment
3. Klicke "Promote to Production"

---

## 🚀 Phase 7: Remote Monitoring Integration

### 7.1 Python Monitoring Client

```python
import requests
import json
from datetime import datetime

def check_stallwache_health():
    """Check Stallwache API health"""
    try:
        response = requests.get(
            'https://stallwache-skill.vercel.app/api/health',
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Stallwache Status: {data['status']}")
            print(f"  Version: {data['version']}")
            print(f"  Uptime: {data['uptime_seconds']}s")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False

def fetch_status():
    """Get current system status"""
    try:
        response = requests.get(
            'https://stallwache-skill.vercel.app/api/status',
            timeout=5
        )
        
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return data
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

# Run checks
if __name__ == "__main__":
    print(f"Checking Stallwache at {datetime.now()}")
    check_stallwache_health()
    print("\nFull Status:")
    fetch_status()
```

### 7.2 JavaScript/Node.js Client

```javascript
// monitoring_client.js

const BASE_URL = 'https://stallwache-skill.vercel.app';

async function checkHealth() {
    try {
        const response = await fetch(`${BASE_URL}/api/health`);
        const data = await response.json();
        
        console.log('✓ Stallwache Status:', data.status);
        console.log('  Version:', data.version);
        console.log('  Uptime:', data.uptime_seconds, 'seconds');
        
        return data.status === 'healthy';
    } catch (error) {
        console.error('✗ Health check failed:', error);
        return false;
    }
}

async function getStatus() {
    try {
        const response = await fetch(`${BASE_URL}/api/status`);
        const data = await response.json();
        console.log(JSON.stringify(data, null, 2));
        return data;
    } catch (error) {
        console.error('✗ Error:', error);
        return null;
    }
}

// Run every 5 minutes
setInterval(async () => {
    console.log(`\nCheck at ${new Date().toISOString()}`);
    await checkHealth();
}, 5 * 60 * 1000);

// Initial check
checkHealth().then(healthy => {
    if (healthy) {
        getStatus();
    }
});
```

---

## 📈 Phase 8: Scaling & Performance

### 8.1 Vercel Pro Features (kostenpflichtig)

```
- Custom Domains: $12/month
- Schnellere Deployments
- Mehr concurrent serverless functions
- Database Support (via Vercel Postgres)
- Enhanced Analytics
```

### 8.2 Performance Optimization

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "devCommand": "python test_vercel_api.py",
  "functions": {
    "vercel_app.py": {
      "memory": 1024,
      "maxDuration": 60,
      "runtime": "python3.11"
    }
  },
  "regions": ["iad1", "sfo1"],
  "env": {
    "PYTHONUNBUFFERED": "1"
  }
}
```

### 8.3 Caching Strategy

```python
# In vercel_app.py handler()
headers = {
    "Content-Type": "application/json",
    "Cache-Control": "public, s-maxage=60",  # Cache 60 Sekunden
    "CDN-Cache-Control": "max-age=3600"     # CDN Cache 1 Stunde
}
```

---

## 🔍 Troubleshooting

### Issue: "Module not found"

**Lösung:**
1. Überprüfe `requirements.txt` hat alle Dependencies
2. Verifiziere Python-Version passt (3.10+)
3. Überprüfe `vercel.json` hat korrekte Build-Konfiguration

```bash
# Check requirements.txt
cat requirements.txt

# Verify locally
pip install -r requirements.txt
```

### Issue: "Function timed out"

**Lösung:**
1. Erhöhe `maxDuration` in `vercel.json`
2. Optimiere Code für Geschwindigkeit
3. Verwende Caching für häufige Requests

```json
{
  "functions": {
    "vercel_app.py": {
      "maxDuration": 120  // Erhöhe auf 120 Sekunden
    }
  }
}
```

### Issue: "Environment variables not loading"

**Lösung:**
1. Verifiziere Variables in Vercel Dashboard gesetzt
2. Redeploy nach Setting der Variables
3. Überprüfe `.env` Files sind in `.gitignore`

```bash
# Überprüfe lokal
python -c "import os; print(os.getenv('CAMERA_RTSP_URL', 'NOT SET'))"
```

### Issue: "Build fails"

**Lösung:**
1. Überprüfe Build Logs in Vercel Dashboard
2. Teste lokal:
   ```bash
   python test_vercel_api.py
   ```
3. Überprüfe Python version (3.11 empfohlen)

### Issue: "API returns 404"

**Lösung:**
1. Überprüfe Endpoint ist korrekt
2. Verifiziere `vercel.json` routes
3. Überprüfe `vercel_app.py` path handling

```bash
# Test lokal
curl http://localhost:3000/api/health
```

---

## 📞 Support & Resources

- **Vercel Docs**: https://vercel.com/docs
- **Python Runtime**: https://vercel.com/docs/functions/python
- **Stallwache GitHub**: https://github.com/stallwache/skill
- **Email**: stallwache123@gmail.com

---

## ✅ Deployment Checklist

- [ ] GitHub Repository mit neuesten Code
- [ ] `vercel_app.py` erstellt und getestet
- [ ] `vercel.json` konfiguriert
- [ ] Environment Variables in Vercel gesetzt
- [ ] Deployment erfolgreich
- [ ] API Endpoints getestet
  - [ ] `/api/health` - antwortet
  - [ ] `/api/status` - zeigt Status
  - [ ] `/api/events` - antwortet
  - [ ] `/api/statistics` - antwortet
  - [ ] `/api/config` - zeigt Konfiguration
- [ ] Custom Domain konfiguriert (optional)
- [ ] Monitoring aktiviert
- [ ] Dokumentation aktualisiert

---

## 🎉 Du bist Live!

Dein Stallwache Deployment ist jetzt:
- ✅ In der Cloud laufend
- ✅ Erreichbar via REST API
- ✅ Auto-Scaling mit Demand
- ✅ Automatisch deployed bei git push
- ✅ Überwacht und gelogt
- ✅ Produktionsreif

**Deine API:**
```
https://stallwache-skill.vercel.app
```

**Teile es:**
- GitHub: stallwache-skill
- Vercel: stallwache-skill.vercel.app
- Marketplace: Cowork Marketplace

---

## 🚀 Nächste Schritte

1. ✅ Phase 1: GitHub - DONE
2. ✅ Phase 2: Vercel - DONE
3. 👉 Phase 3: Marketplace Submission
4. 🎉 LAUNCH: Stallwache LIVE!

---

**Created with ❤️ for Stallwache | v1.0.0-vercel | May 2026**
