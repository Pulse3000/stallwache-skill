#!/usr/bin/env python3
"""
Stallwache Camera Connection Test
Validiere die Verbindung zur Rollei Safetycam HD 20

Kamera-IP: 192.168.178.108:80
RTSP-Stream: rtsp://192.168.178.108:554/stream
"""

import sys
import cv2
import socket
import requests
from urllib.parse import urlparse
from pathlib import Path

# Add parent dir to path
sys.path.insert(0, str(Path(__file__).parent))

from config import CAMERA_RTSP_URL, CAMERA_USERNAME, CAMERA_PASSWORD
from logger import setup_logging, get_logger

logger = get_logger(__name__)


def test_network_connectivity(host: str, port: int) -> bool:
    """Test Netzwerk-Erreichbarkeit."""
    logger.info(f"🔍 Teste Netzwerk-Erreichbarkeit: {host}:{port}")

    try:
        sock = socket.create_connection((host, port), timeout=5)
        sock.close()
        logger.info(f"✓ Host {host}:{port} erreichbar")
        return True
    except socket.timeout:
        logger.error(f"✗ Timeout beim Verbinden zu {host}:{port}")
        return False
    except socket.error as e:
        logger.error(f"✗ Netzwerk-Fehler: {e}")
        return False


def test_http_interface(host: str, port: int, username: str, password: str) -> bool:
    """Test HTTP Web-Interface der Kamera."""
    logger.info(f"🔍 Teste HTTP Web-Interface: {host}:{port}")

    try:
        url = f"http://{host}:{port}/cgi-bin/admin/param.cgi?cmd=getinfo"
        auth = (username, password)

        response = requests.get(url, auth=auth, timeout=10)

        if response.status_code == 200:
            logger.info(f"✓ HTTP Web-Interface antwortet")
            return True
        else:
            logger.warning(f"⚠ HTTP Response: {response.status_code}")
            return False

    except requests.exceptions.Timeout:
        logger.error(f"✗ HTTP Timeout")
        return False
    except requests.exceptions.ConnectionError as e:
        logger.error(f"✗ HTTP Verbindungsfehler: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ HTTP Test Fehler: {e}")
        return False


def test_rtsp_stream(rtsp_url: str) -> bool:
    """Test RTSP-Stream."""
    logger.info(f"🔍 Teste RTSP-Stream: {rtsp_url}")

    try:
        cap = cv2.VideoCapture(rtsp_url)

        if not cap.isOpened():
            logger.error(f"✗ Konnte RTSP-Stream nicht öffnen")
            return False

        # Versuche einen Frame zu lesen
        ret, frame = cap.read()
        cap.release()

        if ret and frame is not None:
            width = frame.shape[1]
            height = frame.shape[0]
            logger.info(f"✓ RTSP-Stream lädt erfolgreich")
            logger.info(f"  → Auflösung: {width}×{height}")
            return True
        else:
            logger.error(f"✗ Konnte keinen Frame aus Stream lesen")
            return False

    except Exception as e:
        logger.error(f"✗ RTSP-Test Fehler: {e}")
        return False


def test_rtsp_with_credentials(rtsp_url: str, username: str, password: str) -> bool:
    """Test RTSP-Stream mit Authentifizierung."""
    logger.info(f"🔍 Teste RTSP mit Authentifizierung")

    try:
        # Konstruiere RTSP-URL mit Credentials
        parsed = urlparse(rtsp_url)
        auth_url = f"rtsp://{username}:{password}@{parsed.netloc}{parsed.path}"

        logger.debug(f"  URL mit Auth: rtsp://[USER]:[PASS]@{parsed.netloc}{parsed.path}")

        cap = cv2.VideoCapture(auth_url)

        if not cap.isOpened():
            logger.error(f"✗ Konnte RTSP-Stream mit Auth nicht öffnen")
            return False

        # Versuche einen Frame zu lesen
        ret, frame = cap.read()
        cap.release()

        if ret and frame is not None:
            width = frame.shape[1]
            height = frame.shape[0]
            logger.info(f"✓ RTSP-Stream mit Authentifizierung lädt erfolgreich")
            logger.info(f"  → Auflösung: {width}×{height}")
            logger.info(f"  → Credentials funktionieren ✓")
            return True
        else:
            logger.error(f"✗ Konnte keinen Frame aus authentifiziertem Stream lesen")
            return False

    except Exception as e:
        logger.error(f"✗ RTSP-Auth Test Fehler: {e}")
        return False


def main():
    """Führe alle Tests durch."""
    setup_logging(level="INFO")

    logger.info("="*60)
    logger.info("🐄 Stallwache Camera Connection Test")
    logger.info("="*60)

    # Parse IP und Port aus RTSP-URL
    parsed = urlparse(CAMERA_RTSP_URL)
    camera_host = parsed.hostname or "192.168.178.108"
    camera_http_port = 80
    camera_rtsp_port = parsed.port or 554

    logger.info(f"\n📋 Kamera-Informationen:")
    logger.info(f"  Host: {camera_host}")
    logger.info(f"  HTTP Port: {camera_http_port}")
    logger.info(f"  RTSP Port: {camera_rtsp_port}")
    logger.info(f"  RTSP URL: {CAMERA_RTSP_URL}")
    logger.info(f"  Username: {CAMERA_USERNAME}")

    # Tests
    results = {}

    logger.info(f"\n{'='*60}")
    logger.info("🧪 Test 1: Netzwerk-Erreichbarkeit (HTTP)")
    logger.info(f"{'='*60}")
    results['network_http'] = test_network_connectivity(camera_host, camera_http_port)

    logger.info(f"\n{'='*60}")
    logger.info("🧪 Test 2: HTTP Web-Interface")
    logger.info(f"{'='*60}")
    results['http_interface'] = test_http_interface(
        camera_host,
        camera_http_port,
        CAMERA_USERNAME,
        CAMERA_PASSWORD
    )

    logger.info(f"\n{'='*60}")
    logger.info("🧪 Test 3: Netzwerk-Erreichbarkeit (RTSP)")
    logger.info(f"{'='*60}")
    results['network_rtsp'] = test_network_connectivity(camera_host, camera_rtsp_port)

    logger.info(f"\n{'='*60}")
    logger.info("🧪 Test 4: RTSP-Stream (ohne Auth)")
    logger.info(f"{'='*60}")
    results['rtsp_noauth'] = test_rtsp_stream(CAMERA_RTSP_URL)

    logger.info(f"\n{'='*60}")
    logger.info("🧪 Test 5: RTSP-Stream (mit Authentifizierung)")
    logger.info(f"{'='*60}")
    results['rtsp_auth'] = test_rtsp_with_credentials(
        CAMERA_RTSP_URL,
        CAMERA_USERNAME,
        CAMERA_PASSWORD
    )

    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("📊 Test Summary")
    logger.info(f"{'='*60}")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status} - {test_name}")

    logger.info(f"\n{'='*60}")

    if passed == total:
        logger.info(f"✓ ALLE TESTS BESTANDEN ({passed}/{total})")
        logger.info(f"\n🚀 System ist bereit für Production-Start!")
        logger.info(f"\nNächste Schritte:")
        logger.info(f"1. docker-compose up -d")
        logger.info(f"   oder")
        logger.info(f"   python main.py")
        logger.info(f"{'='*60}\n")
        return 0
    else:
        logger.error(f"✗ EINIGE TESTS FEHLGESCHLAGEN ({passed}/{total})")
        logger.error(f"\n💡 Troubleshooting:")

        if not results['network_http']:
            logger.error(f"  - HTTP Port 80: Prüfe Netzwerk & Firewall")

        if not results['http_interface']:
            logger.error(f"  - HTTP Interface: Prüfe Benutzername/Passwort")

        if not results['network_rtsp']:
            logger.error(f"  - RTSP Port 554: Prüfe Netzwerk & Firewall")

        if not results['rtsp_noauth']:
            logger.error(f"  - RTSP Stream: Prüfe RTSP-URL")

        if not results['rtsp_auth']:
            logger.error(f"  - RTSP Auth: Prüfe Credentials in .env")

        logger.error(f"{'='*60}\n")
        return 1


if __name__ == "__main__":
    exit(main())
