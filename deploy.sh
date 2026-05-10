#!/bin/bash
# Stallwache Production Deployment Script
# Usage: bash deploy.sh

set -e

echo "🐄 Stallwache Production Deployment"
echo "===================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
DOCKER_IMAGE="stallwache:prod"
CONTAINER_NAME="stallwache"
ENV_FILE=".env.production"

# Functions
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Pre-flight checks
echo -e "\n${YELLOW}1. Pre-flight Checks${NC}"

if [ ! -f "$ENV_FILE" ]; then
    print_error "Konfiguration nicht gefunden: $ENV_FILE"
    echo "   → Kopiere .env.production zu .env"
    exit 1
fi
print_status "Konfiguration vorhanden"

if ! command -v docker &> /dev/null; then
    print_error "Docker nicht installiert"
    exit 1
fi
print_status "Docker verfügbar"

# Load configuration
source "$ENV_FILE"

if [ -z "$CAMERA_RTSP_URL" ]; then
    print_error "CAMERA_RTSP_URL nicht gesetzt"
    exit 1
fi
print_status "Kamera-URL: $CAMERA_RTSP_URL"

if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
    print_warning "Telegram nicht konfiguriert - Alerts deaktiviert"
fi

# Build Docker Image
echo -e "\n${YELLOW}2. Docker Image bauen${NC}"

if docker build -t "$DOCKER_IMAGE" . ; then
    print_status "Docker Image erfolgreich gebaut"
else
    print_error "Docker Build fehlgeschlagen"
    exit 1
fi

# Stop existing container
echo -e "\n${YELLOW}3. Alte Container stoppen${NC}"

if docker ps --filter "name=$CONTAINER_NAME" --format "{{.Names}}" | grep -q "^$CONTAINER_NAME$"; then
    if docker stop "$CONTAINER_NAME"; then
        print_status "Container gestoppt"
    fi

    if docker rm "$CONTAINER_NAME"; then
        print_status "Container entfernt"
    fi
else
    print_warning "Kein laufender Container gefunden"
fi

# Create volumes
echo -e "\n${YELLOW}4. Datenverzeichnisse erstellen${NC}"

mkdir -p logs data models
print_status "Verzeichnisse erstellt"

# Start new container
echo -e "\n${YELLOW}5. Neuen Container starten${NC}"

if docker run -d \
    --name "$CONTAINER_NAME" \
    --restart always \
    --env-file "$ENV_FILE" \
    -v "$(pwd)/logs:/app/logs" \
    -v "$(pwd)/data:/app/data" \
    -v "$(pwd)/models:/app/models" \
    -p 8000:8000 \
    "$DOCKER_IMAGE" ; then
    print_status "Container gestartet"
else
    print_error "Container Start fehlgeschlagen"
    exit 1
fi

# Wait for startup
echo -e "\n${YELLOW}6. Container-Startup warten...${NC}"
sleep 3

# Health check
echo -e "\n${YELLOW}7. Health Check${NC}"

if docker ps --filter "name=$CONTAINER_NAME" --format "{{.Names}}" | grep -q "^$CONTAINER_NAME$"; then
    print_status "Container läuft"
else
    print_error "Container läuft nicht"
    docker logs "$CONTAINER_NAME" | tail -20
    exit 1
fi

# Show logs
echo -e "\n${YELLOW}8. Live Logs (letzten 20 Zeilen)${NC}"
docker logs "$CONTAINER_NAME" | tail -20

# Summary
echo -e "\n${GREEN}===================================="
echo "✓ Deployment erfolgreich!"
echo "====================================${NC}\n"

echo "📋 System-Information:"
echo "   Container: $CONTAINER_NAME"
echo "   Image: $DOCKER_IMAGE"
echo "   Kamera: $CAMERA_RTSP_URL"
echo "   Logs: ./logs/"
echo "   Datenbank: ./data/stallwache.db"
echo "   Metriken: http://localhost:8000/metrics"

echo -e "\n📝 Häufige Befehle:"
echo "   # Logs anschauen"
echo "   docker logs -f $CONTAINER_NAME"
echo ""
echo "   # Container neu starten"
echo "   docker restart $CONTAINER_NAME"
echo ""
echo "   # Container stoppen"
echo "   docker stop $CONTAINER_NAME"
echo ""
echo "   # Status prüfen"
echo "   docker ps -a | grep $CONTAINER_NAME"
echo ""
echo "   # Metriken abrufen"
echo "   curl http://localhost:8000/metrics"
echo ""

echo -e "\n🔗 Links:"
echo "   Telegram Bot: https://t.me/BotFather"
echo "   Kamera-Interface: http://$CAMERA_RTSP_URL (lokal) oder https://stallwache.rolleicam.net"
echo "   Datenbank abfragen: sqlite3 ./data/stallwache.db"
echo ""

print_status "Deployment bereit! System läuft jetzt im Hintergrund."
