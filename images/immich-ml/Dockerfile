# =============================================================================
# SOVEREIGN HARDENED IMMICH-ML
# Generated from template - Version: 1.106.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.106.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 py3-pip python3 ca-certificates curl  \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir --break-system-packages onnxruntime fastapi uvicorn pillow 2>/dev/null || \
    pip3 install --no-cache-dir onnxruntime fastapi uvicorn pillow
RUN useradd -m -u 65532 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 3003
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="immich-ml" \
      org.opencontainers.image.version="1.106.0" \
      org.opencontainers.image.vendor="Immich" \
      org.opencontainers.image.source="https://github.com/immich-app/immich/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM