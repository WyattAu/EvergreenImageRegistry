# =============================================================================
# SOVEREIGN HARDENED CHROMA
# Generated from template - Version: 0.5.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.5.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv ca-certificates git build-essential && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir --break-system-packages chromadb==${VERSION} 2>/dev/null || \
    pip3 install --no-cache-dir --break-system-packages chromadb
RUN useradd -m -u 65534 -g '' chroma 2>/dev/null || true
RUN mkdir -p /app /var/log/chroma /var/cache/chroma && chown -R chroma:chroma /app /var/log/chroma /var/cache/chroma 2>/dev/null || true
USER chroma
WORKDIR /app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8000/api/v1/heartbeat
ENTRYPOINT ["chroma"]
LABEL org.opencontainers.image.title="chroma" \
      org.opencontainers.image.version="0.5.0" \
      org.opencontainers.image.vendor="Chroma" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
