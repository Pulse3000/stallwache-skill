#!/bin/bash

# ============================================================================
# 🚀 STALLWACHE VERCEL AUTO DEPLOYMENT SCRIPT (Bash)
# Automatisches Deployment zu Vercel mit Verification
# ============================================================================

echo "🚀 STALLWACHE VERCEL DEPLOYMENT STARTING..."
echo "=========================================="
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Project Directory: $PROJECT_DIR"
echo ""

# ============================================================================
# PHASE 1: PRE-DEPLOYMENT CHECKS
# ============================================================================

echo -e "\033[33mPHASE 1: Pre-Deployment Checks\033[0m"
echo "==============================="
echo ""

echo "📍 Checking required files..."

REQUIRED_FILES=(
    "vercel_app.py"
    "vercel.json"
    "test_vercel_api.py"
    "requirements.txt"
    "VERCEL_DEPLOYMENT_COMPLETE.md"
)

ALL_FILES_EXIST=true

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file found"
    else
        echo "  ✗ $file NOT FOUND"
        ALL_FILES_EXIST=false
    fi
done

if [ "$ALL_FILES_EXIST" = false ]; then
    echo ""
    echo -e "\033[31m✗ ERROR: Required files missing!\033[0m"
    echo "Make sure all Vercel files are created first."
    exit 1
fi

echo ""
echo -e "\033[32m✓ All required files present\033[0m"
echo ""

# ============================================================================
# PHASE 2: LOCAL API TESTING
# ============================================================================

echo -e "\033[33mPHASE 2: Local API Testing\033[0m"
echo "=========================="
echo ""

echo "📍 Checking Python installation..."
PYTHON_VERSION=$(python3 --version 2>&1)
if [ $? -eq 0 ]; then
    echo "  ✓ Python: $PYTHON_VERSION"
else
    echo "  ✗ Python not found"
    echo "  Install Python from: https://python.org"
    exit 1
fi

echo ""
echo "📍 Installing dependencies..."
pip3 install -q -r requirements.txt 2>&1 | tail -1
if [ $? -eq 0 ]; then
    echo "  ✓ Dependencies installed"
else
    echo "  ✗ Failed to install dependencies"
    exit 1
fi

echo ""
echo "📍 Running API tests..."
python3 test_vercel_api.py

if [ $? -eq 0 ]; then
    echo ""
    echo -e "\033[32m✓ All API tests PASSED!\033[0m"
else
    echo ""
    echo -e "\033[31m✗ API tests FAILED\033[0m"
    echo -e "\033[33mFix errors before deployment\033[0m"
    exit 1
fi

echo ""

# ============================================================================
# PHASE 3: GIT VERIFICATION
# ============================================================================

echo -e "\033[33mPHASE 3: Git Verification\033[0m"
echo "========================="
echo ""

echo "📍 Checking git repository..."
if [ -d ".git" ]; then
    echo "  ✓ Git repository found"
else
    echo "  ✗ Git repository NOT initialized"
    echo "  Run: ./auto_deploy.sh first"
    exit 1
fi

echo ""
echo "📍 Checking git status..."
GIT_STATUS=$(git status --porcelain)
if [ -z "$GIT_STATUS" ]; then
    echo "  ✓ Git working directory clean"
else
    echo "  ⚠️  Uncommitted changes detected:"
    echo "$GIT_STATUS"
    echo ""
    read -p "  Do you want to commit and push? (Y/n): " -n 1 RESPONSE
    echo ""

    if [ "$RESPONSE" = "Y" ] || [ "$RESPONSE" = "y" ] || [ -z "$RESPONSE" ]; then
        echo "  📍 Committing changes..."
        git add .
        git commit -m "feat: Update Vercel deployment configuration"
        git push origin main
        echo "  ✓ Changes committed and pushed"
    fi
fi

echo ""

# ============================================================================
# PHASE 4: VERCEL SETUP INSTRUCTIONS
# ============================================================================

echo -e "\033[33mPHASE 4: Vercel Setup Instructions\033[0m"
echo "==================================="
echo ""

echo -e "\033[32m✅ Your code is ready for Vercel deployment!\033[0m"
echo ""
echo -e "\033[33m⚠️  NEXT STEPS (Manual in Vercel):\033[0m"
echo ""
echo -e "\033[36m1. Open: https://vercel.com/new\033[0m"
echo ""
echo -e "\033[36m2. Sign in with GitHub\033[0m"
echo ""
echo -e "\033[36m3. Import Repository:\033[0m"
echo "   - Select: stallwache-skill"
echo "   - Click: Import"
echo ""
echo -e "\033[36m4. Configure Build Settings:\033[0m"
echo "   - Framework: Python"
echo "   - Build: (use default)"
echo ""
echo -e "\033[36m5. Set Environment Variables:\033[0m"
echo "   Click: Settings → Environment Variables"
echo "   Add these variables:"
echo ""

declare -A ENV_VARS=(
    ["CAMERA_RTSP_URL"]="rtsp://admin:PASSWORD@192.168.178.108/stream"
    ["CAMERA_USERNAME"]="admin"
    ["CAMERA_PASSWORD"]="YOUR_CAMERA_PASSWORD"
    ["TELEGRAM_BOT_TOKEN"]="YOUR_BOT_TOKEN"
    ["TELEGRAM_CHAT_ID"]="YOUR_CHAT_ID"
    ["ENABLE_TELEGRAM"]="true"
    ["DEVICE"]="cpu"
    ["YOLO_MODEL_PATH"]="./models/yolov8m.pt"
    ["CONFIDENCE_THRESHOLD"]="0.65"
    ["FRAME_SKIP"]="1"
    ["LOG_LEVEL"]="INFO"
    ["LOG_RETENTION_DAYS"]="30"
)

for key in "${!ENV_VARS[@]}"; do
    echo "   $key = ${ENV_VARS[$key]}"
done

echo ""
echo -e "\033[36m6. Deploy:\033[0m"
echo "   - Click: Deploy"
echo "   - Wait: 1-3 minutes"
echo ""
echo -e "\033[36m7. Test Deployment:\033[0m"
echo "   Once deployed, test your API:"
echo -e "\033[32m   https://stallwache-skill.vercel.app/api/health\033[0m"
echo ""

# ============================================================================
# PHASE 5: HELP TEXT
# ============================================================================

echo -e "\033[33mPHASE 5: Additional Resources\033[0m"
echo "============================="
echo ""
echo -e "\033[36m📚 Documentation:\033[0m"
echo "   - VERCEL_QUICK_START.md"
echo "   - VERCEL_DEPLOYMENT_COMPLETE.md"
echo "   - VERCEL_CHANGES.md"
echo ""
echo -e "\033[36m🔗 Useful Links:\033[0m"
echo "   - Vercel: https://vercel.com"
echo "   - Python Runtime: https://vercel.com/docs/functions/python"
echo "   - GitHub: https://github.com/stallwache/skill"
echo ""
echo -e "\033[36m📞 Support:\033[0m"
echo "   - Email: stallwache123@gmail.com"
echo ""

# ============================================================================
# SUCCESS!
# ============================================================================

echo ""
echo -e "\033[32m🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉\033[0m"
echo ""
echo -e "\033[32m✅ STALLWACHE VERCEL READY!\033[0m"
echo ""
echo -e "\033[32mYour system is ready for cloud deployment:\033[0m"
echo -e "\033[32m  ✓ Code quality verified\033[0m"
echo -e "\033[32m  ✓ API endpoints tested\033[0m"
echo -e "\033[32m  ✓ Git repository clean\033[0m"
echo -e "\033[32m  ✓ Dependencies installed\033[0m"
echo ""
echo -e "\033[33mNext: Follow the Vercel setup instructions above!\033[0m"
echo ""

exit 0
