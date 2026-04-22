# =============================================================================
# SOVEREIGN HARDENED BAZARR-SUBLIMINAL
# Generated from template - Version: 1.5.2
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.5.2
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv git ca-certificates curl build-essential && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch v1.5.2 https://github.com/morpheus65535/bazarr.git /opt/bazarr-subliminal 2>/dev/null || \
    git clone --depth 1 https://github.com/morpheus65535/bazarr.git /opt/bazarr-subliminal
RUN cd /opt/bazarr-subliminal && \
    pip3 install --no-cache-dir --break-system-packages -r requirements.txt 2>/dev/null || true && pip3 install --no-cache-dir --break-system-packages subliminal 2>/dev/null || true
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 6768
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:6768/health || exit 1
ENTRYPOINT ["python3", "/opt/bazarr-subliminal/bazarr.py"]
LABEL org.opencontainers.image.title="bazarr-subliminal" \
      org.opencontainers.image.version="1.5.2" \
      org.opencontainers.image.vendor="Bazarr" \
      org.opencontainers.image.source="https://github.com/morpheus65535/bazarr.git" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
