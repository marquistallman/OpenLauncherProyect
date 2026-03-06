# Multi-stage build for FreeLauncher
FROM python:3.13-slim as builder

WORKDIR /build

# Copy project files
COPY requirements.txt .
COPY src/ src/
COPY main.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.13-slim

WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    openjdk-17-jre-headless \
    tk \
    python3-tk \
    libx11-6 \
    libxext6 \
    xvfb \
    x11-utils \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copy from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /build/src src/
COPY --from=builder /build/main.py .

# Create app directory for data
RUN mkdir -p /root/.freelauncher

# Create non-root user
RUN useradd -m -u 1000 freelauncher && chown -R freelauncher:freelauncher /app /root/.freelauncher
USER freelauncher

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DISPLAY=:99

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import src.core.minecraft_launcher" || exit 1

# Run application
CMD ["python", "main.py"]
