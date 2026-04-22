# =============================================================================
# SOVEREIGN HARDENED GALLERY3
# Generated from template - Version: 3.0.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv git ca-certificates curl build-essential && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch v3.0.0 https://github.com/gallery/gallery3.git /opt/gallery3 2>/dev/null || \
    git clone --depth 1 https://github.com/gallery/gallery3.git /opt/gallery3
RUN cd /opt/gallery3 && \
    pip3 install --no-cache-dir --break-system-packages -r requirements.txt 2>/dev/null || true 
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8000/health || exit 1
ENTRYPOINT ["python3", "/opt/gallery3/manage.py", "runserver", "0.0.0.0:8000"]
LABEL org.opencontainers.image.title="gallery3" \
      org.opencontainers.image.version="3.0.0" \
      org.opencontainers.image.vendor="Gallery" \
      org.opencontainers.image.source="https://github.com/gallery/gallery3.git" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
