"""
Database Module für Stallwache
SQLite-Datenbank für Events und Metriken
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

from logger import get_logger
from config import DATABASE_PATH, LOG_RETENTION_DAYS

logger = get_logger(__name__)


class Database:
    """SQLite Datenbank-Manager."""

    SCHEMA_VERSION = 1

    def __init__(self, db_path: Path = DATABASE_PATH):
        """
        Initialisiere Datenbank.

        Args:
            db_path: Pfad zur SQLite-Datei
        """
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None

        logger.info(f"Database initialisiert | Path: {self.db_path}")

    def initialize(self) -> bool:
        """Initialisiere Datenbankschema."""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row

            cursor = self.connection.cursor()

            # Erstelle Tabellen
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    confidence REAL,
                    frame_number INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    description TEXT,
                    extra_data TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    fps REAL,
                    cpu_percent REAL,
                    memory_percent REAL,
                    frame_count INTEGER,
                    alert_count INTEGER,
                    stream_errors INTEGER
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    frame_number INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    detected_classes TEXT,
                    confidence REAL,
                    bbox_data TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    level TEXT,
                    message TEXT,
                    source TEXT
                )
            """)

            # Erstelle Indices für bessere Performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_events_timestamp
                ON events(timestamp)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_events_type
                ON events(event_type)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_metrics_timestamp
                ON metrics(timestamp)
            """)

            self.connection.commit()
            logger.info("✓ Datenbankschema erstellt")

            # Aufräumen: Alte Einträge löschen
            self._cleanup_old_records()

            return True

        except sqlite3.Error as e:
            logger.error(f"Datenbank-Fehler: {e}")
            return False

    def log_event(
        self,
        event_type: str,
        confidence: Optional[float] = None,
        frame_number: Optional[int] = None,
        timestamp: Optional[datetime] = None,
        description: Optional[str] = None,
        extra_data: Optional[Dict] = None
    ) -> bool:
        """Protokolliere Event."""
        try:
            cursor = self.connection.cursor()

            extra_json = json.dumps(extra_data) if extra_data else None
            ts = (timestamp or datetime.now()).isoformat()

            cursor.execute("""
                INSERT INTO events
                (event_type, confidence, frame_number, timestamp, description, extra_data)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (event_type, confidence, frame_number, ts, description, extra_json))

            self.connection.commit()
            return True

        except sqlite3.Error as e:
            logger.error(f"Fehler beim Event-Logging: {e}")
            return False

    def log_detection(
        self,
        frame_number: int,
        detected_classes: List[str],
        confidence: float,
        bbox_data: Optional[Dict] = None
    ) -> bool:
        """Protokolliere Detektion."""
        try:
            cursor = self.connection.cursor()
            classes_json = json.dumps(detected_classes)
            bbox_json = json.dumps(bbox_data) if bbox_data else None

            cursor.execute("""
                INSERT INTO detections
                (frame_number, detected_classes, confidence, bbox_data)
                VALUES (?, ?, ?, ?)
            """, (frame_number, classes_json, confidence, bbox_json))

            self.connection.commit()
            return True

        except sqlite3.Error as e:
            logger.error(f"Fehler beim Detection-Logging: {e}")
            return False

    def log_metrics(
        self,
        fps: Optional[float] = None,
        cpu_percent: Optional[float] = None,
        memory_percent: Optional[float] = None,
        frame_count: Optional[int] = None,
        alert_count: Optional[int] = None,
        stream_errors: Optional[int] = None
    ) -> bool:
        """Protokolliere System-Metriken."""
        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                INSERT INTO metrics
                (fps, cpu_percent, memory_percent, frame_count, alert_count, stream_errors)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (fps, cpu_percent, memory_percent, frame_count, alert_count, stream_errors))

            self.connection.commit()
            return True

        except sqlite3.Error as e:
            logger.error(f"Fehler beim Metrics-Logging: {e}")
            return False

    def get_events(
        self,
        event_type: Optional[str] = None,
        hours: int = 24,
        limit: int = 100
    ) -> List[Dict]:
        """Hole Events aus Datenbank."""
        try:
            cursor = self.connection.cursor()

            since = (datetime.now() - timedelta(hours=hours)).isoformat()

            if event_type:
                query = """
                    SELECT * FROM events
                    WHERE event_type = ? AND timestamp >= ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """
                cursor.execute(query, (event_type, since, limit))
            else:
                query = """
                    SELECT * FROM events
                    WHERE timestamp >= ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """
                cursor.execute(query, (since, limit))

            return [dict(row) for row in cursor.fetchall()]

        except sqlite3.Error as e:
            logger.error(f"Fehler beim Event-Abruf: {e}")
            return []

    def get_calving_events(self, days: int = 7) -> List[Dict]:
        """Hole alle Kalbungs-Events der letzten N Tage."""
        return self.get_events(
            event_type="CALVING_DETECTED",
            hours=days * 24,
            limit=500
        )

    def get_metrics_summary(self, hours: int = 24) -> Dict:
        """Hole Metriken-Zusammenfassung."""
        try:
            cursor = self.connection.cursor()

            since = (datetime.now() - timedelta(hours=hours)).isoformat()

            cursor.execute("""
                SELECT
                    AVG(fps) as avg_fps,
                    MAX(fps) as max_fps,
                    MIN(fps) as min_fps,
                    AVG(cpu_percent) as avg_cpu,
                    AVG(memory_percent) as avg_memory,
                    SUM(alert_count) as total_alerts,
                    COUNT(*) as sample_count
                FROM metrics
                WHERE timestamp >= ?
            """, (since,))

            row = cursor.fetchone()
            if row:
                return {
                    'avg_fps': row[0],
                    'max_fps': row[1],
                    'min_fps': row[2],
                    'avg_cpu': row[3],
                    'avg_memory': row[4],
                    'total_alerts': row[5] or 0,
                    'sample_count': row[6]
                }
            return {}

        except sqlite3.Error as e:
            logger.error(f"Fehler beim Metriken-Abruf: {e}")
            return {}

    def _cleanup_old_records(self) -> bool:
        """Lösche alte Einträge älter als LOG_RETENTION_DAYS."""
        try:
            cursor = self.connection.cursor()
            cutoff_date = (datetime.now() - timedelta(days=LOG_RETENTION_DAYS)).isoformat()

            # Lösche alte Events
            cursor.execute("""
                DELETE FROM events WHERE timestamp < ?
            """, (cutoff_date,))

            # Lösche alte Metriken
            cursor.execute("""
                DELETE FROM metrics WHERE timestamp < ?
            """, (cutoff_date,))

            # Lösche alte Detektionen
            cursor.execute("""
                DELETE FROM detections WHERE timestamp < ?
            """, (cutoff_date,))

            deleted_count = cursor.rowcount
            self.connection.commit()

            if deleted_count > 0:
                logger.info(f"✓ {deleted_count} alte Datensätze gelöscht")

            return True

        except sqlite3.Error as e:
            logger.error(f"Fehler beim Aufräumen: {e}")
            return False

    def close(self):
        """Schließe Datenbankverbindung."""
        if self.connection:
            self.connection.close()
            logger.info("✓ Datenbank geschlossen")
