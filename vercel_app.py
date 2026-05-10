#!/usr/bin/env python3
"""
Stallwache Vercel Serverless Handler
REST API für Kalberkennungs-System mit Vercel-Unterstützung

Author: Stallwache Team
Version: 1.0.0 Vercel Edition
License: MIT
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='[%(asctime)s] %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StallwacheAPI:
    """REST API für Stallwache Monitoring und Status"""

    def __init__(self):
        """Initialisiere API"""
        self.initialized = False
        self.start_time = datetime.now()

        logger.info("✓ Stallwache API initialisiert")
        self.initialized = True

    def health_check(self) -> Dict[str, Any]:
        """Health Check Endpoint"""
        try:
            uptime = (datetime.now() - self.start_time).total_seconds()
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "uptime_seconds": int(uptime),
                "version": "1.0.0-vercel",
                "camera": "configured" if os.getenv('CAMERA_RTSP_URL') else "not_configured",
                "api": "REST v1"
            }
        except Exception as e:
            logger.error(f"Health check error: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }

    def get_status(self) -> Dict[str, Any]:
        """Aktuelle System-Status"""
        try:
            return {
                "status": "running",
                "timestamp": datetime.now().isoformat(),
                "system": {
                    "version": "1.0.0",
                    "deployment": "vercel",
                    "environment": os.getenv('ENVIRONMENT', 'production'),
                    "region": os.getenv('VERCEL_REGION', 'iad1')
                },
                "camera": {
                    "configured": bool(os.getenv('CAMERA_RTSP_URL')),
                    "protocol": "RTSP"
                },
                "detection": {
                    "model": os.getenv('YOLO_MODEL_PATH', 'yolov8m.pt'),
                    "confidence_threshold": float(os.getenv('CONFIDENCE_THRESHOLD', 0.65)),
                    "device": os.getenv('DEVICE', 'cpu'),
                    "frame_skip": int(os.getenv('FRAME_SKIP', 1))
                },
                "messaging": {
                    "telegram_enabled": os.getenv('ENABLE_TELEGRAM', 'true').lower() == 'true',
                    "configured": bool(os.getenv('TELEGRAM_BOT_TOKEN'))
                },
                "database": {
                    "type": "sqlite",
                    "retention_days": int(os.getenv('LOG_RETENTION_DAYS', 30))
                }
            }
        except Exception as e:
            logger.error(f"Status error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def get_events(self, hours: int = 24) -> Dict[str, Any]:
        """Erkennungs-Events der letzten N Stunden"""
        try:
            since = datetime.now() - timedelta(hours=hours)

            return {
                "status": "success",
                "query": {
                    "hours": hours,
                    "since": since.isoformat(),
                    "until": datetime.now().isoformat()
                },
                "results": {
                    "count": 0,
                    "events": [],
                    "note": "Lokale Datenbank in Vercel serverless nicht persistent. Verwende externe DB für Production."
                }
            }
        except Exception as e:
            logger.error(f"Events error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def get_statistics(self, days: int = 30) -> Dict[str, Any]:
        """Statistiken der letzten N Tage"""
        try:
            return {
                "status": "success",
                "query": {
                    "days": days,
                    "period": f"Last {days} days",
                    "since": (datetime.now() - timedelta(days=days)).isoformat()
                },
                "statistics": {
                    "total_events": 0,
                    "total_alerts": 0,
                    "avg_daily_events": 0,
                    "detection_rate": "0.0%",
                    "uptime_percent": "100.0%",
                    "note": "Lokale Datenbank in Vercel serverless nicht persistent. Verwende externe DB für Production."
                }
            }
        except Exception as e:
            logger.error(f"Statistics error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def get_config(self) -> Dict[str, Any]:
        """Konfiguration anzeigen (ohne Secrets)"""
        try:
            return {
                "status": "success",
                "configuration": {
                    "camera": {
                        "protocol": "RTSP",
                        "credentials": "configured" if os.getenv('CAMERA_USERNAME') else "not_configured"
                    },
                    "telegram": {
                        "enabled": os.getenv('ENABLE_TELEGRAM', 'true').lower() == 'true',
                        "status": "configured" if os.getenv('TELEGRAM_BOT_TOKEN') else "not_configured"
                    },
                    "detection": {
                        "model": os.getenv('YOLO_MODEL_PATH', 'yolov8m.pt'),
                        "confidence_threshold": float(os.getenv('CONFIDENCE_THRESHOLD', 0.65)),
                        "device": os.getenv('DEVICE', 'cpu'),
                        "frame_skip": int(os.getenv('FRAME_SKIP', 1))
                    },
                    "logging": {
                        "level": os.getenv('LOG_LEVEL', 'INFO'),
                        "retention_days": int(os.getenv('LOG_RETENTION_DAYS', 30))
                    },
                    "deployment": {
                        "type": "vercel-serverless",
                        "version": "1.0.0",
                        "python_version": "3.11"
                    }
                }
            }
        except Exception as e:
            logger.error(f"Config error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }


# Globale API-Instanz
api = StallwacheAPI()


async def handler(request):
    """Haupthandler für Vercel HTTP-Requests"""

    path = request.path if hasattr(request, 'path') else request.url.path
    method = request.method if hasattr(request, 'method') else 'GET'

    # Query-Parameter extrahieren
    query_params = {}
    if hasattr(request, 'query'):
        query_params = request.query
    elif hasattr(request.url, 'query'):
        import urllib.parse
        query_params = urllib.parse.parse_qs(request.url.query)

    logger.info(f"Request: {method} {path}")

    # Route Requests
    try:
        if path in ["/api/health", "/health"]:
            return {
                "status": 200,
                "body": json.dumps(api.health_check()),
                "headers": {"Content-Type": "application/json"}
            }

        elif path in ["/api/status", "/status"]:
            return {
                "status": 200,
                "body": json.dumps(api.get_status()),
                "headers": {"Content-Type": "application/json"}
            }

        elif path.startswith("/api/events"):
            # Extract hours parameter
            hours = 24
            if "hours" in query_params:
                try:
                    hours = int(query_params["hours"][0] if isinstance(query_params["hours"], list) else query_params["hours"])
                except (ValueError, TypeError):
                    hours = 24

            return {
                "status": 200,
                "body": json.dumps(api.get_events(hours)),
                "headers": {"Content-Type": "application/json"}
            }

        elif path.startswith("/api/statistics"):
            # Extract days parameter
            days = 30
            if "days" in query_params:
                try:
                    days = int(query_params["days"][0] if isinstance(query_params["days"], list) else query_params["days"])
                except (ValueError, TypeError):
                    days = 30

            return {
                "status": 200,
                "body": json.dumps(api.get_statistics(days)),
                "headers": {"Content-Type": "application/json"}
            }

        elif path == "/api/config":
            return {
                "status": 200,
                "body": json.dumps(api.get_config()),
                "headers": {"Content-Type": "application/json"}
            }

        elif path in ["/", ""]:
            return {
                "status": 200,
                "body": json.dumps({
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
                }),
                "headers": {"Content-Type": "application/json"}
            }

        else:
            return {
                "status": 404,
                "body": json.dumps({
                    "error": "Not Found",
                    "path": path,
                    "available_endpoints": [
                        "/api/health",
                        "/api/status",
                        "/api/events?hours=24",
                        "/api/statistics?days=30",
                        "/api/config"
                    ]
                }),
                "headers": {"Content-Type": "application/json"}
            }

    except Exception as e:
        logger.error(f"Request handler error: {e}", exc_info=True)
        return {
            "status": 500,
            "body": json.dumps({
                "error": "Internal Server Error",
                "message": str(e)
            }),
            "headers": {"Content-Type": "application/json"}
        }


# Für lokales Testing
if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI, Request

    app = FastAPI()

    @app.get("/{full_path:path}")
    @app.post("/{full_path:path}")
    async def root(request: Request, full_path: str = ""):
        request.path = f"/{full_path}"
        return await handler(request)

    logger.info("Starte Stallwache API Server auf http://0.0.0.0:3000")
    uvicorn.run(app, host="0.0.0.0", port=3000)
