# STALLWACHE
## Hardware-Setup-Guide
### Rollei Safetycam HD 20 Integration

**KI-basiertes Kalberkennungs- und Stallüberwachungssystem**

Version 1.0 | Mai 2026

---

## 1. Systemübersicht

Das Stallwache-System besteht aus drei Hauptkomponenten:

- **Rollei Safetycam HD 20** – Netzwerk-Überwachungskamera
- **Edge-Server (lokaler PC/Laptop)** – KI-Inferenz und Alert-Verarbeitung
- **Rollei Cloud & Messenger** – Backup-Speicher und Benachrichtigungen

---

## 2. Rollei Safetycam HD 20 – Technische Spezifikationen

### 2.1 Hardware-Specs

| Parameter | Wert |
|-----------|------|
| Auflösung | 1920×1080 Pixel (Full HD) |
| Framerate | 30 fps bei Full HD |
| Sensor | 1/3″ CMOS |
| Blickwinkel | 160° diagonal (Wide-Angle) |
| Nachtsicht | Infrarot-LEDs (bis 15m) |
| Stromversorgung | 12V DC / PoE (Power over Ethernet) |
| Wasserschutz | IP66 (staub- und wasserdicht) |
| Betriebstemp. | -10°C bis +50°C |
| Gewicht | ca. 280g |
| Abmessungen | 180×108×86 mm |

### 2.2 Netzwerk-Features

- **RTSP-Stream:** `rtsp://[CAMERA_IP]:554/stream`
- **ONVIF-Support:** Standardisierte Geräte-Integration
- **HTTP-API:** Web-Interface für Konfiguration
- **Cloud-Integration:** Automatische Uploads zur Rollei Cloud
- **WiFi 802.11ac (5GHz/2.4GHz):** oder Gigabit Ethernet

---

## 3. Netzwerk-Konfiguration

### 3.1 Schritt 1: Kamera-Initialisierung

1. Stromversorgung anschließen (12V DC oder PoE-Switch)
2. Warten Sie 30 Sekunden auf Boot
3. LED sollte blau/grün blinken (Verbindung wird hergestellt)
4. Standardmäßig versucht die Kamera, sich über DHCP ins Netzwerk einzubuchen

### 3.2 IP-Adresse ermitteln

#### Methode A: Rollei Setup-App

1. Laden Sie die "Rollei SafetyCam" App herunter
2. App scannt automatisch das lokale Netzwerk nach der Kamera
3. Notieren Sie die angezeigte IP-Adresse (z.B. 192.168.1.100)

#### Methode B: Router-Admin-Panel

1. Öffnen Sie Ihren Router-Admin-Panel (meist 192.168.1.1 oder 192.168.0.1)
2. Navigieren Sie zu "Verbundene Geräte" oder "DHCP-Clients"
3. Suchen Sie nach einem Gerät namens "Rollei" oder mit MAC-Adresse beginnend mit 00:1A:AB
4. Notieren Sie die zugewiesene IP-Adresse

### 3.3 Statische IP-Adresse zuweisen

Um zu verhindern, dass sich die Kamera-IP ändert:

1. Öffnen Sie das Web-Interface der Kamera:
   - Browser → `http://[CAMERA_IP]`
   - Standard-Login: `admin` / `12345`

2. Navigieren Sie zu Einstellungen → Netzwerk
3. Wählen Sie "Statische IP" statt DHCP
4. **Empfehlung:** 192.168.1.200 (idealerweise außerhalb des DHCP-Bereichs)
5. Speichern und Kamera neu starten

### 3.4 RTSP-Stream testen

Öffnen Sie einen VLC Media Player:

1. Datei → Stream öffnen
2. URL eingeben:
   - `rtsp://admin:12345@192.168.1.200:554/stream`
3. Wenn Video startet ✓ – RTSP funktioniert

---

## 4. Kamera-Platzierung im Stall

### 4.1 Optimale Positionierung

- **Höhe:** 2–3m (übersichtlicher Blick auf Tier)
- **Winkel:** 45° nach unten gerichtet (Blick auf Flanke und Paar)
- **Entfernung:** 2–5m zum Kalb-Abkalbe-Bereich
- **Vermeiden Sie:** Gegenlicht, Reflektionen auf Sensor

### 4.2 Stromversorgung & Kabelführung

- Verwenden Sie ein separates 12V-Netzteil oder PoE-Injektor
- Kabelführung: Entlang der Stallwand (nicht über Tier-Bewegungsraum)
- Netzwerk-Kabel (Cat5e/Cat6): Min. 10m Reichweite üblich
- Empfehlung: Versorgungsleitungen mit Schutzkanal schützen

### 4.3 Lichtverhältnisse

- **Tagsüber:** Natürliches Licht ausreichend
- **Nachts:** IR-LEDs der Kamera reichen bis 15m
- **Optional:** Zusätzliche IR-Beleuchtung (880nm) für verbesserte Erkennung

---

## 5. Edge-Server (Lokaler PC) – Anforderungen

### 5.1 Mindestanforderungen

| Komponente | Anforderung |
|------------|-------------|
| CPU | Intel i5/i7 oder AMD Ryzen 5/7 (mind. 4 Cores) |
| RAM | 8 GB (16 GB empfohlen für YOLOv8) |
| GPU | Optional: NVIDIA GPU (RTX 3060 oder besser) |
| Speicher | 250 GB SSD (für Logs, Modelle, Puffer) |
| OS | Windows 10/11, Linux (Ubuntu 20.04+), macOS 11+ |
| Netzwerk | Gigabit Ethernet oder 5GHz WiFi |
| RAM-Auslastung | ~2–4 GB während KI-Verarbeitung |
| CPU-Auslastung | ~30–60% bei 30fps 1080p Inferenz |

### 5.2 Software-Setup

1. **Python 3.10+** installieren

2. **Dependencies:**
   - `opencv-python` (Video-Stream)
   - `ultralytics` (YOLOv8)
   - `python-telegram-bot` (Messenger-Integration)
   - `requests` (HTTP-Requests)

3. **Installation:**
   ```bash
   pip install opencv-python ultralytics python-telegram-bot requests
   ```

---

## 6. Netzwerk-Architektur

### 6.1 Topologie

```
┌─────────────────────────────────────────────────────────────┐
│                    Rollei Safetycam HD 20                  │
│              RTSP Stream: rtsp://192.168.1.200:554/...     │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│            LocalPC / Edge-Server (Python)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │  RTSP Client │→ │  Frame Grab  │→ │  YOLOv8 Calving │ │
│  │  (OpenCV)    │  │  + Preproc   │  │  Model Inference│ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
│                                              │              │
│                                              ▼              │
│                    ┌─────────────────────────────────────┐ │
│                    │  Alert Engine (Confidence Scoring) │ │
│                    │  + Telegram/Email Notification      │ │
│                    └─────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
   ┌─────────┐          ┌──────────────┐
   │ Rollei  │          │ Messenger    │
   │ Cloud   │          │ (Telegram)   │
   │ (Backup)│          │ (Alert)      │
   └─────────┘          └──────────────┘
```

### 6.2 Bandbreitenanforderungen

| Komponente | Bandbreite |
|------------|-----------|
| 1080p @ 30fps | ~4 Mbps (komprimiert H.264) |
| Cloud-Backup (intermittent) | ~10 Mbps Peak |
| Messenger-Alerts | <1 Mbps |
| **Gesamtbedarf** | **~15 Mbps (typisch), 20+ Mbps Peak** |

**Empfehlung:** 25+ Mbps Internetverbindung für stabile Verarbeitung

---

## 7. Sicherheit & Datenschutz

### 7.1 Kamera-Sicherheit

- **Standard-Passwort ändern!** Web-Interface: `admin` → [Sicheres Passwort]
- **Firewall-Regel:** Kamera nur im lokalen Netzwerk erreichbar
- **RTSP-Authentifizierung:** Credentials im Stream verwenden
- **Firmware aktuell halten:** Rollei-Sicherheits-Updates regelmäßig prüfen

### 7.2 Daten-Speicherung & Backup

- **Lokale Videobuffer:** 24h = ~400 GB (1080p @ 1 Mbps durchschnittlich)
- **Rollei Cloud:** Tagesübersicht + Alert-Trigger-Videos
- **Retention-Policy:** Lokal 7 Tage, Cloud 30 Tage

### 7.3 DSGVO & Datenschutz

- Video-Verarbeitung ist lokal (kein direkter Cloud-Stream ohne Zustimmung)
- Nur Tier-Bilder werden analysiert (keine Erfassung von Personen)
- Optional: VPN-Tunnel zur Cloud für verschlüsselte Backup-Übertragung

---

## 8. Troubleshooting

| Problem | Lösung |
|---------|--------|
| Kamera antwortet nicht | 1) Stromversorgung prüfen<br>2) Router neu starten<br>3) Kamera neu booten (Power-Knopf 10s) |
| RTSP-Stream stützt ab | 1) Netzwerk-Stabilität prüfen (Ping zur Kamera)<br>2) WiFi → Ethernet wechseln<br>3) PC-Firewall-Einstellungen prüfen |
| Niedriges Video-FPS | 1) Edge-Server-Ressourcen (CPU/RAM) überprüfen<br>2) Streaming-Qualität im Web-Interface reduzieren<br>3) GPU beschleunigung aktivieren |
| Cloud-Upload schlägt fehl | 1) Rollei-Cloud-Login prüfen<br>2) Internetverbindung testen<br>3) Cloud-Speicherplatz überprüfen |

---

## 9. Installation Checkliste

### Hardware

- ☐ Rollei Safetycam HD 20 ausgepackt
- ☐ 12V Netzteil / PoE-Injektor angeschlossen
- ☐ Netzwerk-Kabel verlegt
- ☐ Kamera-Halterung im Stall montiert

### Netzwerk

- ☐ Kamera-IP ermittelt
- ☐ Statische IP konfiguriert
- ☐ RTSP-Stream in VLC getestet
- ☐ Firewall-Regel hinzugefügt
- ☐ Standard-Passwort geändert

### Edge-Server

- ☐ Python 3.10+ installiert
- ☐ Dependencies installiert
- ☐ YOLOv8-Modell heruntergeladen
- ☐ Telegram Bot-Token konfiguriert

---

## Nächste Schritte

Nach erfolgreicher Hardware-Installation:

1. Konsultieren Sie den **Python-Code-Guide** für KI-Inferenz
2. **Docker-Container** für einfaches Deployment aufsetzen
3. Testen Sie die **Kalberkennungs-Modelle** mit Testvideos
4. **Fine-Tune** das Alert-Schwellenwert-System basierend auf echten Stallbedingungen

---

**Support & Kontakt**

Fragen oder Probleme? Kontaktieren Sie: **stallwache123@gmail.com**
