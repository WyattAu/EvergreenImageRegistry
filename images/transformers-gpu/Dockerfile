# =============================================================================
# EVERGREEN HARDENED TRANSFORMERS-GPU
# Generated from template - Version: 4.46.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.46.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates curl && \
    pip install --no-cache-dir --break-system-packages transformers torch 2>/dev/null || \
    pip install --no-cache-dir transformers torch && \
    adduser -u 65532 -D app 2>/dev/null || true && \
    mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8000/ || exit 1
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="transformers-gpu" \
      org.opencontainers.image.description="transformers-gpu container image" \
      org.opencontainers.image.version="4.46.0" \
      org.opencontainers.image.vendor="HuggingFace" \
      org.opencontainers.image.source="https://github.com/huggingface/transformers" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
