"""
Telegram Client Module
Sende Alerts und Benachrichtigungen via Telegram Bot
"""

import cv2
import numpy as np
import io
import time
from typing import Optional
from datetime import datetime
from telegram import Bot, Update
from telegram.error import TelegramError

from logger import get_logger
from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    TELEGRAM_SEND_IMAGE,
    TELEGRAM_ALERT_COOLDOWN,
)

logger = get_logger(__name__)


class TelegramClient:
    """Client für Telegram-Integration."""

    def __init__(self):
        """Initialisiere Telegram Client."""
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.chat_id = TELEGRAM_CHAT_ID
        self.last_alert_time = None
        self.alert_count = 0
        self.cooldown = TELEGRAM_ALERT_COOLDOWN

        logger.info(f"TelegramClient initialisiert | Chat ID: {self.chat_id}")

    def test_connection(self) -> bool:
        """Teste Telegram-Verbindung."""
        try:
            me = self.bot.get_me()
            logger.info(f"✓ Telegram-Verbindung erfolgreich | Bot: {me.first_name}")
            return True
        except TelegramError as e:
            logger.error(f"❌ Telegram-Verbindung fehler: {e}")
            return False

    def send_alert(
        self,
        event_type: str,
        confidence: float,
        frame_number: int,
        frame_image: Optional[np.ndarray] = None
    ) -> bool:
        """
        Sende Alert via Telegram.

        Args:
            event_type: Typ des Events (z.B. "CALVING")
            confidence: Konfidenz-Score
            frame_number: Frame-Nummer
            frame_image: Optional Frame-Bild

        Returns:
            Success status
        """
        # Cooldown-Prüfung (verhindere Alert-Spam)
        if self.last_alert_time:
            elapsed = time.time() - self.last_alert_time
            if elapsed < self.cooldown:
                logger.debug(
                    f"Alert Cooldown aktiv ({elapsed:.0f}/{self.cooldown}s). "
                    f"Überspringe Alert."
                )
                return False

        try:
            self.alert_count += 1

            # Nachricht komponieren
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = self._compose_alert_message(
                event_type=event_type,
                confidence=confidence,
                frame_number=frame_number,
                timestamp=timestamp,
                alert_number=self.alert_count
            )

            # Sende Nachricht
            if TELEGRAM_SEND_IMAGE and frame_image is not None:
                self._send_with_image(message, frame_image)
            else:
                self.bot.send_message(chat_id=self.chat_id, text=message)

            self.last_alert_time = time.time()
            logger.info(f"✓ Telegram-Alert gesendet | {event_type}")
            return True

        except TelegramError as e:
            logger.error(f"❌ Fehler beim Senden von Telegram-Alert: {e}")
            return False

    def _compose_alert_message(
        self,
        event_type: str,
        confidence: float,
        frame_number: int,
        timestamp: str,
        alert_number: int
    ) -> str:
        """Komponiere Alert-Nachricht."""
        message = (
            f"🚨 <b>STALLWACHE ALERT</b>\n\n"
            f"<b>Event:</b> {event_type}\n"
            f"<b>Konfidenz:</b> {confidence:.1%}\n"
            f"<b>Frame:</b> #{frame_number}\n"
            f"<b>Zeit:</b> {timestamp}\n"
            f"<b>Alert #:</b> {alert_number}\n\n"
            f"<i>Bitte überprüfe den Stall sofort!</i>"
        )
        return message

    def _send_with_image(self, message: str, frame: np.ndarray) -> bool:
        """Sende Alert mit Bild."""
        try:
            # Konvertiere Frame zu JPEG
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                logger.warning("Konnte Frame nicht zu JPEG kodieren")
                self.bot.send_message(chat_id=self.chat_id, text=message)
                return True

            # Sende Photo mit Caption
            image_bytes = io.BytesIO(jpeg.tobytes())
            self.bot.send_photo(
                chat_id=self.chat_id,
                photo=image_bytes,
                caption=message,
                parse_mode='HTML'
            )
            return True

        except TelegramError as e:
            logger.error(f"Fehler beim Senden von Bild: {e}")
            # Fallback: Sende nur Text
            try:
                self.bot.send_message(chat_id=self.chat_id, text=message)
                return True
            except:
                return False

    def send_status(self, status_info: dict) -> bool:
        """Sende Status-Update."""
        try:
            message = (
                f"📊 <b>Stallwache Status Update</b>\n\n"
                f"<b>Uptime:</b> {status_info.get('uptime', 'N/A')}\n"
                f"<b>Frames verarbeitet:</b> {status_info.get('frames_processed', 0)}\n"
                f"<b>Alerts gesendet:</b> {status_info.get('alerts_sent', 0)}\n"
                f"<b>Durchschn. Konfidenz:</b> {status_info.get('avg_confidence', 0):.1%}\n"
                f"<b>CPU-Auslastung:</b> {status_info.get('cpu_usage', 'N/A')}\n"
                f"<b>RAM-Auslastung:</b> {status_info.get('ram_usage', 'N/A')}\n"
            )

            self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode='HTML')
            logger.info("✓ Status-Update gesendet")
            return True

        except TelegramError as e:
            logger.error(f"Fehler beim Senden von Status: {e}")
            return False

    def send_error(self, error_message: str) -> bool:
        """Sende Error-Benachrichtigung."""
        try:
            message = (
                f"⚠️ <b>STALLWACHE ERROR</b>\n\n"
                f"<b>Fehler:</b> {error_message}\n"
                f"<b>Zeit:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"<i>Bitte überprüfe das System!</i>"
            )

            self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode='HTML')
            logger.info("✓ Error-Nachricht gesendet")
            return True

        except TelegramError as e:
            logger.error(f"Fehler beim Senden von Error-Nachricht: {e}")
            return False

    def get_statistics(self) -> dict:
        """Liefere Telegram-Statistiken."""
        return {
            'alerts_sent': self.alert_count,
            'last_alert_time': self.last_alert_time,
            'cooldown_seconds': self.cooldown,
        }
