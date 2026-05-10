#!/bin/bash
# Stallwache Health Check Script
# Überwache System-Status und Kamera-Verbindung

set -e

CONTAINER_NAME="stallwache"
CAMERA_IP="192.168.178.108"
CAMERA_HTTP_PORT=80
CAMERA_RTSP_PORT=554
METRICS_PORT=8000

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}$1${NC}"
    echo "════════════════════════════════════════════════════════"
}

print_ok() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Header
clear
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║  🐄 STALLWACHE HEALTH CHECK                           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"

# 1. Docker Container Status
print_header "1. DOCKER CONTAINER"

if docker ps --filter "name=$CONTAINER_NAME" --format "{{.Names}}" | grep -q "^$CONTAINER_NAME$"; then
    print_ok "Container läuft"

    # Get container uptime
    UPTIME=$(docker inspect --format='{{.State.StartedAt}}' $CONTAINER_NAME)
    print_ok "Startzeit: $UPTIME"

    # CPU & Memory
    STATS=$(docker stats --no-stream $CONTAINER_NAME 2>/dev/null)
    if [ $? -eq 0 ]; then
        CPU=$(echo "$STATS" | awk 'NR==2 {print $3}')
        MEM=$(echo "$STATS" | awk 'NR==2 {print $4}')
        print_ok "CPU: $CPU | RAM: $MEM"
    fi
else
    print_error "Container läuft NICHT"
    echo "         Start mit: docker-compose up -d"
fi

# 2. Kamera Netzwerk
print_header "2. KAMERA NETZWERK"

if timeout 5 bash -c "cat < /dev/null > /dev/tcp/$CAMERA_IP/$CAMERA_HTTP_PORT" 2>/dev/null; then
    print_ok "HTTP Port 80 erreichbar"
else
    print_error "HTTP Port 80 NICHT erreichbar"
    echo "         IP: $CAMERA_IP"
fi

if timeout 5 bash -c "cat < /dev/null > /dev/tcp/$CAMERA_IP/$CAMERA_RTSP_PORT" 2>/dev/null; then
    print_ok "RTSP Port 554 erreichbar"
else
    print_warning "RTSP Port 554 NICHT erreichbar (normal wenn durch NAT)"
fi

# Ping
if ping -c 1 -W 2 $CAMERA_IP &> /dev/null; then
    PING=$(ping -c 3 -W 2 $CAMERA_IP 2>/dev/null | tail -1 | awk '{print $4}' | cut -d'/' -f2)
    print_ok "Ping zu Kamera: ${PING}ms"
else
    print_error "Ping zu Kamera fehlgeschlagen"
fi

# 3. Container Logs
print_header "3. CONTAINER LOGS (letzte 10 Zeilen)"

if docker ps --filter "name=$CONTAINER_NAME" --format "{{.Names}}" | grep -q "^$CONTAINER_NAME$"; then
    docker logs --tail 10 $CONTAINER_NAME 2>&1 | while read line; do
        if [[ $line =~ ERROR|error ]]; then
            echo -e "${RED}$line${NC}"
        elif [[ $line =~ WARNING|warning ]]; then
            echo -e "${YELLOW}$line${NC}"
        else
            echo "$line"
        fi
    done
else
    print_warning "Container läuft nicht, Logs nicht verfügbar"
fi

# 4. Metrics
print_header "4. SYSTEM METRIKEN"

if curl -s http://localhost:$METRICS_PORT/metrics &> /dev/null; then
    print_ok "Metriken-Endpunkt erreichbar (Port $METRICS_PORT)"

    # Parse metrics
    FRAMES=$(curl -s http://localhost:$METRICS_PORT/metrics 2>/dev/null | grep "frames_processed" | head -1 | awk '{print $2}')
    FPS=$(curl -s http://localhost:$METRICS_PORT/metrics 2>/dev/null | grep "frames_per_second" | head -1 | awk '{print $2}')
    ALERTS=$(curl -s http://localhost:$METRICS_PORT/metrics 2>/dev/null | grep "alerts_sent" | head -1 | awk '{print $2}')

    if [ ! -z "$FRAMES" ]; then
        print_ok "Frames verarbeitet: $FRAMES"
    fi
    if [ ! -z "$FPS" ]; then
        print_ok "FPS: $FPS"
    fi
    if [ ! -z "$ALERTS" ]; then
        print_ok "Alerts gesendet: $ALERTS"
    fi
else
    print_error "Metriken-Endpunkt nicht erreichbar"
fi

# 5. Datenbank
print_header "5. DATENBANK"

if [ -f "data/stallwache.db" ]; then
    print_ok "Datenbank-Datei existiert"

    # Event Count
    EVENT_COUNT=$(sqlite3 data/stallwache.db "SELECT COUNT(*) FROM events;" 2>/dev/null)
    print_ok "Events in Datenbank: $EVENT_COUNT"

    # Last Event
    LAST_EVENT=$(sqlite3 data/stallwache.db "SELECT event_type, timestamp FROM events ORDER BY timestamp DESC LIMIT 1;" 2>/dev/null)
    if [ ! -z "$LAST_EVENT" ]; then
        print_ok "Letztes Event: $LAST_EVENT"
    fi

    # Calving Count
    CALVING_COUNT=$(sqlite3 data/stallwache.db "SELECT COUNT(*) FROM events WHERE event_type='CALVING_DETECTED';" 2>/dev/null)
    print_ok "Kalbungen erkannt: $CALVING_COUNT"
else
    print_warning "Datenbank-Datei nicht gefunden"
fi

# 6. Logs
print_header "6. LOG-DATEIEN"

if [ -d "logs" ]; then
    MAIN_LOG=$(ls -lh logs/stallwache.log 2>/dev/null | awk '{print $5, $9}')
    if [ ! -z "$MAIN_LOG" ]; then
        print_ok "Hauptlog: $MAIN_LOG"
    fi

    ERROR_LOG=$(ls -lh logs/stallwache_error.log 2>/dev/null | awk '{print $5, $9}')
    if [ ! -z "$ERROR_LOG" ]; then
        ERRORS=$(wc -l < logs/stallwache_error.log 2>/dev/null)
        if [ "$ERRORS" -gt 0 ]; then
            print_warning "Fehlerlog: $ERROR_LOG ($ERRORS Zeilen)"
        else
            print_ok "Fehlerlog: $ERROR_LOG"
        fi
    fi
else
    print_warning "Logs-Verzeichnis nicht gefunden"
fi

# 7. Disk Space
print_header "7. SPEICHERPLATZ"

DISK_USAGE=$(du -sh . 2>/dev/null | cut -f1)
print_ok "Stallwache Größe: $DISK_USAGE"

DATA_SIZE=$(du -sh data/ 2>/dev/null | cut -f1)
print_ok "Datenbank-Größe: $DATA_SIZE"

LOGS_SIZE=$(du -sh logs/ 2>/dev/null | cut -f1)
print_ok "Logs-Größe: $LOGS_SIZE"

# Summary
print_header "ZUSAMMENFASSUNG"

CONTAINER_OK=false
CAMERA_OK=false
METRICS_OK=false
DATABASE_OK=false

docker ps --filter "name=$CONTAINER_NAME" --format "{{.Names}}" | grep -q "^$CONTAINER_NAME$" && CONTAINER_OK=true
timeout 5 bash -c "cat < /dev/null > /dev/tcp/$CAMERA_IP/$CAMERA_HTTP_PORT" 2>/dev/null && CAMERA_OK=true
curl -s http://localhost:$METRICS_PORT/metrics &> /dev/null && METRICS_OK=true
[ -f "data/stallwache.db" ] && DATABASE_OK=true

if $CONTAINER_OK && $CAMERA_OK && $METRICS_OK && $DATABASE_OK; then
    echo -e "\n${GREEN}"
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║  ✓ SYSTEM HEALTHY - Alles läuft optimal!             ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo -e "${NC}\n"
    exit 0
else
    echo -e "\n${YELLOW}"
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║  ⚠ EINIGE CHECKS FEHLGESCHLAGEN                       ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo -e "${NC}\n"

    echo "Status Übersicht:"
    [ "$CONTAINER_OK" = true ] && echo -e "  ${GREEN}✓${NC} Container" || echo -e "  ${RED}✗${NC} Container"
    [ "$CAMERA_OK" = true ] && echo -e "  ${GREEN}✓${NC} Kamera" || echo -e "  ${RED}✗${NC} Kamera"
    [ "$METRICS_OK" = true ] && echo -e "  ${GREEN}✓${NC} Metriken" || echo -e "  ${RED}✗${NC} Metriken"
    [ "$DATABASE_OK" = true ] && echo -e "  ${GREEN}✓${NC} Datenbank" || echo -e "  ${RED}✗${NC} Datenbank"
    echo ""

    exit 1
fi
