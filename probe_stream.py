#!/usr/bin/env python3
"""
STALLWACHE – Kamera Stream-Probe Script
Testet alle bekannten URL-Pfade der Rollei SafetyCam 20 HD
und gibt den funktionierenden Stream-Pfad aus.

Usage:
    python3 probe_stream.py
    python3 probe_stream.py --ip 192.168.178.108 --user Stallwache123! --pwd Stallwache123!
"""

import argparse
import urllib.request
import urllib.error
import socket
import time
import sys

# ── Kamera-Einstellungen ────────────────────────────────────────────────────
DEFAULT_IP   = "192.168.178.108"
DEFAULT_USER = "Stallwache123!"
DEFAULT_PWD  = "Stallwache123!"
TIMEOUT      = 5

# ── Bekannte Stream-Pfade ───────────────────────────────────────────────────
STREAM_PATHS = [
    # ── Rollei SafetyCam 20 HD (via iSpyConnect BESTÄTIGT) ──
    "/videostream.asf?user={user}&pwd={pwd}&resolution=1280x720",
    "/videostream.asf?user={user}&pwd={pwd}&resolution=640x480",
    "/videostream.cgi?user={user}&pwd={pwd}&resolution=1280x720",
    "/videostream.cgi?user={user}&pwd={pwd}&resolution=640x480",
    # ── Snapshot ──
    "/snapshot.cgi?user={user}&pwd={pwd}",
    "/cgi-bin/snapshot.cgi?user={user}&pwd={pwd}",
    # ── MJPEG Fallback ──
    "/mjpeg?user={user}&pwd={pwd}",
    "/mjpegstream.cgi?user={user}&pwd={pwd}",
    "/video.cgi?user={user}&pwd={pwd}",
]

GREEN  = "\033[92m"; RED = "\033[91m"; YELLOW = "\033[93m"
RESET  = "\033[0m";  BOLD = "\033[1m"

def probe_url(url, timeout=TIMEOUT):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "StallwacheProbe/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code  = resp.getcode()
            ctype = resp.headers.get("Content-Type", "unknown")
            data  = resp.read(512)
            return (len(data) > 0, code, ctype)
    except urllib.error.HTTPError as e:
        return False, e.code, str(e.reason)
    except urllib.error.URLError as e:
        return False, 0, str(e.reason)
    except socket.timeout:
        return False, 0, "timeout"
    except Exception as e:
        return False, 0, str(e)

def main():
    parser = argparse.ArgumentParser(description="Stallwache – Kamera Stream-Probe")
    parser.add_argument("--ip",   default=DEFAULT_IP)
    parser.add_argument("--user", default=DEFAULT_USER)
    parser.add_argument("--pwd",  default=DEFAULT_PWD)
    parser.add_argument("--port", default=80, type=int)
    args = parser.parse_args()

    base = f"http://{args.ip}:{args.port}"
    print(f"\n{BOLD}🐄 STALLWACHE – Stream-Probe{RESET}")
    print(f"{'─'*55}")
    print(f"  Kamera:    {args.ip}:{args.port}")
    print(f"  Benutzer:  {args.user}")
    print(f"  Timeout:   {TIMEOUT}s pro Pfad")
    print(f"{'─'*55}\n")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex((args.ip, args.port))
    sock.close()
    if result != 0:
        print(f"{RED}✗ Kamera nicht erreichbar auf {args.ip}:{args.port}{RESET}")
        sys.exit(1)
    print(f"{GREEN}✓ Kamera erreichbar!{RESET}\n")

    working = []
    for path_template in STREAM_PATHS:
        path    = path_template.format(user=args.user, pwd=args.pwd)
        url     = f"{base}{path}"
        display = f"{base}{path_template.format(user=args.user, pwd='***')}"
        print(f"  → {display[:75]:<75}", end="", flush=True)
        ok, code, ctype = probe_url(url)
        if ok:
            print(f"  {GREEN}✓ HTTP {code} | {ctype}{RESET}")
            working.append((url, display, ctype))
        else:
            label = f"HTTP {code}" if code else ctype
            print(f"  {RED}✗ {label}{RESET}")
        time.sleep(0.3)

    print(f"\n{'─'*55}")
    if working:
        print(f"\n{GREEN}{BOLD}✅ {len(working)} funktionierender Stream-Pfad(e) gefunden:{RESET}\n")
        for url, display, ctype in working:
            print(f"  🎥 {display}")
            print(f"     Content-Type: {ctype}\n")
        best_url = working[0][0]
        print(f"{BOLD}📋 .env Eintrag:{RESET}")
        print(f"  STREAM_URL={best_url}")
    else:
        print(f"\n{RED}✗ Kein Stream gefunden.{RESET}")
        print(f"  → Webinterface prüfen: http://{args.ip}")
    print(f"\n{'─'*55}\n")

if __name__ == "__main__":
    main()
