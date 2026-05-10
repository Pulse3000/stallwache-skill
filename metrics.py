"""
Metrics Module für Performance-Tracking
"""

import time
from typing import Dict
from collections import deque
from datetime import datetime

from logger import get_logger

logger = get_logger(__name__)


class MetricsCollector:
    """Sammelt und verwaltet Performance-Metriken."""

    def __init__(self, window_size: int = 100):
        """
        Initialisiere Metrics Collector.

        Args:
            window_size: Größe des Sliding Window für Durchschnittswerte
        """
        self.window_size = window_size
        self.frame_count = 0
        self.alert_count = 0
        self.start_time = time.time()

        # Sliding Windows für gleitende Durchschnitte
        self.frame_times = deque(maxlen=window_size)
        self.inference_times = deque(maxlen=window_size)

        logger.info("MetricsCollector initialisiert")

    def update_frame_count(self, frame_number: int):
        """Aktualisiere Frame-Zähler."""
        self.frame_count = frame_number

    def increment_alerts(self):
        """Erhöhe Alert-Zähler."""
        self.alert_count += 1

    def record_frame_time(self, elapsed_time: float):
        """Protokolliere Frame-Verarbeitungszeit."""
        self.frame_times.append(elapsed_time)

    def record_inference_time(self, elapsed_time: float):
        """Protokolliere Inferenz-Zeit."""
        self.inference_times.append(elapsed_time)

    def get_fps(self) -> float:
        """Berechne aktuelle FPS."""
        if not self.frame_times:
            return 0.0

        # FPS = 1 / durchschnittliche Frame-Zeit
        avg_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_time if avg_time > 0 else 0.0

    def get_avg_inference_time(self) -> float:
        """Berechne durchschnittliche Inferenz-Zeit (ms)."""
        if not self.inference_times:
            return 0.0

        return (sum(self.inference_times) / len(self.inference_times)) * 1000

    def get_alert_count(self) -> int:
        """Liefere Gesamt-Alert-Zähler."""
        return self.alert_count

    def get_uptime(self) -> float:
        """Berechne Uptime in Sekunden."""
        return time.time() - self.start_time

    def get_statistics(self) -> Dict:
        """Liefere vollständige Metriken-Statistik."""
        uptime = self.get_uptime()
        fps = self.get_fps()
        avg_inference = self.get_avg_inference_time()

        return {
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': uptime,
            'uptime_hours': uptime / 3600,
            'frames_processed': self.frame_count,
            'frames_per_second': fps,
            'alerts_sent': self.alert_count,
            'avg_inference_ms': avg_inference,
            'frame_buffer_size': len(self.frame_times),
        }

    def print_statistics(self):
        """Drucke Metriken aus."""
        stats = self.get_statistics()

        print("\n" + "="*60)
        print("📊 STALLWACHE PERFORMANCE METRICS")
        print("="*60)
        print(f"Uptime: {stats['uptime_hours']:.1f} hours")
        print(f"Frames processed: {stats['frames_processed']:,}")
        print(f"FPS: {stats['frames_per_second']:.1f}")
        print(f"Alerts sent: {stats['alerts_sent']}")
        print(f"Avg inference time: {stats['avg_inference_ms']:.1f}ms")
        print("="*60 + "\n")
