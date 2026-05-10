# Stallwache Docker Image
# Production-ready Container für KI-basierte Kalberkennungs-System

FROM python:3.11-slim

# Setze Working Directory
WORKDIR /app

# Installiere System-Dependencies
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Kopiere Requirements
COPY requirements.txt .

# Installiere Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere Anwendungscode
COPY . .

# Erstelle notwendige Verzeichnisse
RUN mkdir -p logs data models

# Health Check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/metrics || exit 1

# Environment Variables
ENV PYTHONUNBUFFERED=1
ENV DEVICE=cpu
ENV LOG_LEVEL=INFO

# Entrypoint
ENTRYPOINT ["python", "main.py"]
