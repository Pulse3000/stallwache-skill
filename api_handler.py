#!/usr/bin/env python3
"""
Stallwache API Handler for Vercel Deployment
Exposes Stallwache monitoring as REST API endpoints
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

# Import Stallwache modules
try:
    from config import Config
    from database import Database
    from detector import YOLODetector
    from stream_processor import RTSPProcessor
    from telegram_client import TelegramClient
    from metrics import Metrics
except ImportError as e:
    logger.error(f"Failed to import Stallwache modules: {e}")
    raise


class StallwacheAPI:
    """REST API interface for Stallwache monitoring"""

    def __init__(self):
        """Initialize API with configuration"""
        self.config = Config()
        self.db = Database(self.config)
        self.metrics = Metrics()
        self.detector = YOLODetector(self.config)
        self.telegram = TelegramClient(self.config) if self.config.enable_telegram else None

        logger.info("Stallwache API initialized")

    def health_check(self) -> Dict[str, Any]:
        """Health check endpoint"""
        try:
            uptime = self.metrics.get_uptime()
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "uptime_seconds": uptime,
                "version": "1.0.0",
                "camera": "configured" if self.config.camera_rtsp_url else "not_configured"
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }

    def get_status(self) -> Dict[str, Any]:
        """Get current system status"""
        try:
            metrics = self.metrics.get_current()

            return {
                "status": "running",
                "timestamp": datetime.now().isoformat(),
                "metrics": {
                    "fps": metrics.get('fps', 0),
                    "inference_time_ms": metrics.get('inference_time_ms', 0),
                    "frames_processed": metrics.get('frames_processed', 0),
                    "detections_total": metrics.get('detections_total', 0),
                    "alerts_sent": metrics.get('alerts_sent', 0)
                },
                "camera": {
                    "rtsp_url": self.config.camera_rtsp_url,
                    "connected": True  # Would need actual check
                },
                "telegram": {
                    "enabled": self.config.enable_telegram,
                    "connected": self.telegram is not None
                }
            }
        except Exception as e:
            logger.error(f"Status check failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def get_events(self, hours: int = 24) -> Dict[str, Any]:
        """Get detection events from last N hours"""
        try:
            since = datetime.now() - timedelta(hours=hours)
            events = self.db.get_events_since(since)

            return {
                "status": "success",
                "query": {
                    "hours": hours,
                    "since": since.isoformat()
                },
                "results": {
                    "count": len(events),
                    "events": [
                        {
                            "id": e.id,
                            "timestamp": e.timestamp.isoformat(),
                            "confidence": e.confidence,
                            "alert_sent": e.alert_sent
                        }
                        for e in events
                    ]
                }
            }
        except Exception as e:
            logger.error(f"Failed to get events: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def get_statistics(self, days: int = 30) -> Dict[str, Any]:
        """Get statistics for last N days"""
        try:
            stats = self.db.get_statistics(days)

            return {
                "status": "success",
                "query": {
                    "days": days,
                    "period": f"Last {days} days"
                },
                "statistics": {
                    "total_events": stats.get('total_events', 0),
                    "total_alerts": stats.get('total_alerts', 0),
                    "avg_daily_events": stats.get('avg_daily_events', 0),
                    "detection_rate": f"{stats.get('detection_rate', 0):.1f}%",
                    "uptime_percent": f"{stats.get('uptime_percent', 0):.1f}%"
                }
            }
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration (without secrets)"""
        return {
            "status": "success",
            "configuration": {
                "camera": {
                    "rtsp_url": self.config.camera_rtsp_url[:30] + "..." if self.config.camera_rtsp_url else None,
                    "credentials": "configured" if self.config.camera_username else "not_configured"
                },
                "telegram": {
                    "enabled": self.config.enable_telegram,
                    "token": "configured" if self.config.telegram_bot_token else "not_configured"
                },
                "detection": {
                    "model": self.config.yolo_model_path,
                    "confidence_threshold": self.config.confidence_threshold,
                    "device": self.config.device,
                    "frame_skip": self.config.frame_skip
                },
                "database": {
                    "type": "sqlite",
                    "retention_days": self.config.log_retention_days
                }
            }
        }


# ============================================================================
# VERCEL HANDLER FUNCTIONS
# ============================================================================

# Initialize API once
api = StallwacheAPI()


async def handler(request):
    """Main request handler for Vercel"""

    path = request.path
    method = request.method

    logger.info(f"Request: {method} {path}")

    # Routes
    if path == "/api/health" or path == "/health":
        return {
            "status": 200,
            "body": json.dumps(api.health_check()),
            "headers": {"Content-Type": "application/json"}
        }

    elif path == "/api/status" or path == "/status":
        return {
            "status": 200,
            "body": json.dumps(api.get_status()),
            "headers": {"Content-Type": "application/json"}
        }

    elif path.startswith("/api/events"):
        hours = int(request.query.get("hours", [24])[0])
        return {
            "status": 200,
            "body": json.dumps(api.get_events(hours)),
            "headers": {"Content-Type": "application/json"}
        }

    elif path.startswith("/api/statistics"):
        days = int(request.query.get("days", [30])[0])
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

    elif path == "/" or path == "":
        return {
            "status": 200,
            "body": json.dumps({
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
            }),
            "headers": {"Content-Type": "application/json"}
        }

    else:
        return {
            "status": 404,
            "body": json.dumps({"error": "Not Found"}),
            "headers": {"Content-Type": "application/json"}
        }


# For local testing
if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Stallwache API server...")

    app = lambda: handler
    uvicorn.run(app, host="0.0.0.0", port=3000)
