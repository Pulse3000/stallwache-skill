"""
Logging Module für Stallwache
Zentrale Log-Verwaltung mit Rotating File Handler
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional

from config import LOG_DIR, LOG_LEVEL, LOG_MAX_SIZE, LOG_BACKUP_COUNT


class ColoredFormatter(logging.Formatter):
    """Custom Formatter mit Farb-Support für Console."""

    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'

    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
        return super().format(record)


def setup_logging(level: str = LOG_LEVEL) -> logging.Logger:
    """
    Initialisiere globales Logging-System.

    Args:
        level: Log-Level (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Configured logger instance
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Entferne existierende Handler
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Log-Format
    log_format = (
        "%(asctime)s | %(name)s | %(levelname)-8s | %(message)s"
    )
    date_format = "%Y-%m-%d %H:%M:%S"

    # ==================
    # Console Handler
    # ==================
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = ColoredFormatter(log_format, datefmt=date_format)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # ==================
    # File Handler (Rotating)
    # ==================
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / "stallwache.log"

    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file,
        maxBytes=LOG_MAX_SIZE,
        backupCount=LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_formatter = logging.Formatter(log_format, datefmt=date_format)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    # ==================
    # Error File Handler
    # ==================
    error_file = LOG_DIR / "stallwache_error.log"
    error_handler = logging.handlers.RotatingFileHandler(
        filename=error_file,
        maxBytes=LOG_MAX_SIZE,
        backupCount=LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    root_logger.addHandler(error_handler)

    root_logger.info(f"Logging initialisiert | Level: {level}")
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Erstelle Logger für spezifisches Modul.

    Args:
        name: Module name (üblicherweise __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
