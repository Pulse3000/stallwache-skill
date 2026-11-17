#!/bin/bash
# Alle Pruefungen dieses Repos in einem Lauf:  bash pruefen.sh
#
# Pures Python – cv2, numpy und ultralytics werden in den Tests gestubbt.
# NICHTS installieren. Nicht Teil dieses Laufs (brauchen Kamera bzw. Pakete):
# test_camera.py, test_vercel_api.py, probe_stream.py.
set -uo pipefail
cd "$(dirname "$0")"

fehl=0
lauf() {
  echo "=== $*"
  if ! "$@"; then
    fehl=$((fehl + 1))
    echo "ROT: $*"
  fi
}

# Uebersetzbar? (faengt Syntaxfehler in Dateien ohne Test)
lauf python3 -m py_compile config.py database.py detector.py logger.py main.py \
  metrics.py stream_processor.py telegram_client.py vercel_app.py paket_bauen.py

# Kalbung nur mit Modell-Befund
lauf python3 test_detector_evidenz.py

# Kein Kamera-Passwort im Log
lauf python3 test_stream_log.py

# Veroeffentlichtes Paket entspricht dem Repo-Stand
lauf python3 paket_bauen.py --pruefen

find . -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null

echo
if [ "$fehl" -eq 0 ]; then
  echo "ALLE PRUEFUNGEN GRUEN"
else
  echo "$fehl PRUEFUNG(EN) ROT"
  exit 1
fi
