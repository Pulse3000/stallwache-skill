#!/usr/bin/env python3
"""
Lokales Test-Script für Stallwache Vercel API

Verwendung:
    python test_vercel_api.py
"""

import os
import sys
import json
import asyncio
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from vercel_app import api, handler


class MockRequest:
    """Simuliert einen Vercel Request für lokales Testing"""

    def __init__(self, path: str, method: str = "GET", query_params: dict = None):
        self.path = path
        self.method = method
        self.query = query_params or {}
        self.url = self

    class URL:
        def __init__(self):
            self.query = ""


async def test_endpoints():
    """Teste alle Endpoints"""

    print("\n" + "="*60)
    print("🧪 STALLWACHE VERCEL API TEST")
    print("="*60 + "\n")

    test_cases = [
        ("/", "GET", "Root Endpoint"),
        ("/api/health", "GET", "Health Check"),
        ("/api/status", "GET", "Status"),
        ("/api/events", "GET", "Events (default 24h)"),
        ("/api/events", "GET", "Events (custom 48h)"),
        ("/api/statistics", "GET", "Statistics (default 30d)"),
        ("/api/config", "GET", "Configuration"),
    ]

    results = []

    for path, method, description in test_cases:
        try:
            print(f"Testing: {description}")
            print(f"  Endpoint: {method} {path}")

            # Create mock request
            if "events" in path:
                query = {"hours": ["48"]} if "custom" in description else {"hours": ["24"]}
            elif "statistics" in path:
                query = {"days": ["30"]}
            else:
                query = {}

            request = MockRequest(path, method, query)

            # Call handler
            response = await handler(request)

            # Parse response
            status_code = response.get("status", 500)
            body = json.loads(response.get("body", "{}"))

            # Check status
            success = status_code == 200

            # Display result
            status_emoji = "✓" if success else "✗"
            print(f"  Status: {status_emoji} {status_code}")

            if body.get("error"):
                print(f"  Error: {body['error']}")
            else:
                print(f"  Response: {body.get('status', body.get('name', 'OK'))}")

            results.append({
                "endpoint": f"{method} {path}",
                "description": description,
                "status": status_code,
                "success": success
            })

            print()

        except Exception as e:
            print(f"  ✗ ERROR: {e}\n")
            results.append({
                "endpoint": f"{method} {path}",
                "description": description,
                "status": 500,
                "success": False,
                "error": str(e)
            })

    # Summary
    print("="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for r in results if r["success"])
    total = len(results)

    for result in results:
        status_emoji = "✓" if result["success"] else "✗"
        print(
            f"{status_emoji} {result['endpoint']:30} "
            f"{result['status']:3} | {result['description']}"
        )

    print("\n" + "="*60)
    print(f"PASSED: {passed}/{total}")
    print("="*60 + "\n")

    return passed == total


if __name__ == "__main__":
    # Set environment variables for testing
    os.environ["CAMERA_RTSP_URL"] = "rtsp://192.168.178.108/stream"
    os.environ["CAMERA_USERNAME"] = "admin"
    os.environ["ENABLE_TELEGRAM"] = "true"
    os.environ["LOG_LEVEL"] = "INFO"

    # Run tests
    success = asyncio.run(test_endpoints())

    # Exit code
    sys.exit(0 if success else 1)
