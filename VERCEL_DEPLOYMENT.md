# 🚀 Stallwache Vercel Deployment Guide

Deploy Stallwache to Vercel for cloud-based monitoring and REST API access.

---

## 📋 Prerequisites

- ✅ GitHub repository created (stallwache-skill)
- ✅ All code pushed to GitHub
- ✅ Vercel account (free at https://vercel.com)
- ✅ Git configured on your computer

---

## 🎯 What You Get with Vercel

```
✓ Cloud hosting (serverless)
✓ REST API endpoints
✓ Real-time monitoring dashboard
✓ Auto-scaling
✓ Custom domain support
✓ Environment variables management
✓ Automatic deployments on git push
✓ Free tier available
```

---

## 🔧 Step 1: Prepare GitHub Repository

### 1.1 Add Vercel Configuration Files

These files are already created:
- ✅ `vercel.json` - Vercel configuration
- ✅ `api_handler.py` - REST API endpoints

### 1.2 Push to GitHub

```bash
git add vercel.json api_handler.py
git commit -m "feat: Add Vercel deployment configuration"
git push origin main
```

---

## 🌐 Step 2: Deploy to Vercel

### 2.1 Create Vercel Account

1. Open: https://vercel.com
2. Sign up with GitHub
3. Authorize Vercel to access your GitHub repos

### 2.2 Import GitHub Repository

1. Dashboard → "Add New..." → "Project"
2. Select your GitHub account
3. Find and select: `stallwache-skill`
4. Click "Import"

### 2.3 Configure Environment Variables

Vercel will ask for environment variables. Add these:

```
CAMERA_RTSP_URL = rtsp://admin:Stallwache123!@192.168.178.108/stream
CAMERA_USERNAME = admin
CAMERA_PASSWORD = Stallwache123!
TELEGRAM_BOT_TOKEN = your_bot_token_here
TELEGRAM_CHAT_ID = your_chat_id_here
ENABLE_TELEGRAM = true
DEVICE = cpu
YOLO_MODEL_PATH = ./models/yolov8m.pt
CONFIDENCE_THRESHOLD = 0.65
FRAME_SKIP = 1
LOG_LEVEL = INFO
LOG_RETENTION_DAYS = 30
```

### 2.4 Deploy

1. Click "Deploy"
2. Wait for deployment to complete (2-5 minutes)
3. You'll get a URL like: `https://stallwache-skill.vercel.app`

---

## 🌍 Step 3: Access Your Deployment

### 3.1 Visit Your Deployment

Go to: `https://stallwache-skill.vercel.app`

You should see:
```json
{
  "name": "Stallwache",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {
    "health": "/api/health",
    "status": "/api/status",
    "events": "/api/events?hours=24",
    "statistics": "/api/statistics?days=30",
    "config": "/api/config"
  }
}
```

### 3.2 Test API Endpoints

**Health Check:**
```
https://stallwache-skill.vercel.app/api/health
```

**Current Status:**
```
https://stallwache-skill.vercel.app/api/status
```

**Events (last 24 hours):**
```
https://stallwache-skill.vercel.app/api/events?hours=24
```

**Statistics (last 30 days):**
```
https://stallwache-skill.vercel.app/api/statistics?days=30
```

**Configuration:**
```
https://stallwache-skill.vercel.app/api/config
```

---

## 🔐 Step 4: Secure Your Deployment

### 4.1 Add Custom Domain (Optional)

1. Vercel Dashboard → Project Settings → Domains
2. Add your domain or use Vercel's subdomain
3. Configure DNS if needed

### 4.2 Enable Authentication (Optional)

```bash
# Add protection in vercel.json
"env": {
  "API_KEY": "@api_key"
}
```

Then require API key in requests:
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://stallwache-skill.vercel.app/api/status
```

---

## 📊 Step 5: Monitor Your Deployment

### 5.1 Vercel Dashboard

1. Go to: https://vercel.com/dashboard
2. Select your project: `stallwache-skill`
3. View:
   - Deployment history
   - Build logs
   - Performance metrics
   - Analytics

### 5.2 Real-Time Logs

```bash
# Install Vercel CLI
npm install -g vercel

# View logs
vercel logs stallwache-skill --follow
```

---

## 🔄 Step 6: Automatic Deployments

### 6.1 Git Integration

Every time you push to GitHub:
```bash
git add .
git commit -m "fix: Improve detection accuracy"
git push origin main
```

Vercel automatically:
1. Detects the change
2. Builds the project
3. Deploys to production
4. Updates your API

### 6.2 Preview Deployments

Push to a new branch:
```bash
git checkout -b feature/new-endpoint
git push origin feature/new-endpoint
```

Vercel creates a preview URL automatically for testing before merging to `main`.

---

## 🚀 Step 7: Monitor Remotely

### 7.1 Health Monitoring

Create a monitoring script:

```bash
#!/bin/bash

# Monitor Stallwache health every 5 minutes
while true; do
    STATUS=$(curl -s https://stallwache-skill.vercel.app/api/health)
    
    if echo $STATUS | grep -q "healthy"; then
        echo "✓ Stallwache is healthy"
    else
        echo "✗ Stallwache is unhealthy"
        # Send alert
    fi
    
    sleep 300  # 5 minutes
done
```

### 7.2 Alert Integration

Add to your monitoring:

```python
import requests
import json

def check_stallwache():
    try:
        response = requests.get('https://stallwache-skill.vercel.app/api/status')
        data = response.json()
        
        if data['status'] == 'running':
            fps = data['metrics']['fps']
            detections = data['metrics']['detections_total']
            
            print(f"FPS: {fps}")
            print(f"Total Detections: {detections}")
        else:
            print("ERROR: Stallwache not running!")
            # Send alert
            
    except Exception as e:
        print(f"Failed to check status: {e}")

# Run every 5 minutes
check_stallwache()
```

---

## 📈 Step 8: Scale Your Deployment

### 8.1 Pro Features (Paid)

- Custom domains: $12/month
- Faster deployments
- More concurrent serverless functions
- Database support

### 8.2 Optimize for Scale

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "functions": {
    "api_handler.py": {
      "memory": 1024,
      "maxDuration": 60
    }
  }
}
```

---

## 🔍 Troubleshooting

### Issue: "Module not found"

**Solution:**
1. Check `requirements.txt` has all dependencies
2. Verify Python version matches (3.10+)
3. Check vercel.json has correct build configuration

### Issue: "Function timed out"

**Solution:**
1. Reduce FRAME_SKIP
2. Use smaller YOLO model (yolov8s.pt instead of yolov8m.pt)
3. Increase maxDuration in vercel.json

### Issue: "Environment variables not loading"

**Solution:**
1. Verify variables set in Vercel Dashboard
2. Redeploy after setting variables
3. Check .env files are in .gitignore

### Issue: "Camera connection fails"

**Solution:**
1. Ensure camera is accessible from internet
2. Check RTSP URL is correct
3. Verify network has proper port forwarding

---

## 📞 Support

- Vercel Docs: https://vercel.com/docs
- Stallwache GitHub: https://github.com/stallwache/skill
- Email: stallwache123@gmail.com

---

## ✅ Deployment Checklist

- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Vercel account created
- [ ] Repository imported to Vercel
- [ ] Environment variables configured
- [ ] Deployment successful
- [ ] API endpoints tested
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up
- [ ] Documentation updated

---

## 🎉 You're Live!

Your Stallwache deployment is now:
- ✅ Running in the cloud
- ✅ Accessible via REST API
- ✅ Auto-scaling with demand
- ✅ Automatically deployed on git push
- ✅ Monitored and logged

**Your API:**
```
https://stallwache-skill.vercel.app
```

**Share it:**
- GitHub: stallwache-skill
- Vercel: stallwache-skill.vercel.app
- Marketplace: Cowork Marketplace

---

**Next Steps:**
1. ✅ Phase 1: GitHub - DONE
2. ✅ Phase 2: Vercel - DONE
3. 👉 Phase 3: Marketplace Submission
4. 🎉 Launch: Stallwache LIVE!

---

Created with ❤️ for Stallwache | v1.0.0 | May 2026
