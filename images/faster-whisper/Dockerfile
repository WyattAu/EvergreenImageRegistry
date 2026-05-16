# =============================================================================
# EVERGREEN HARDENED FASTER-WHISPER
# Generated from template - Version: 1.1.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.1.1
ARG TARGETARCH
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates wget python3 py3-pip 2>/dev/null || apk add --no-cache ca-certificates wget python3 pip 2>/dev/null || true & \
    pip install --no-cache-dir --break-system-packages faster-whisper 2>/dev/null || \
    pip install --no-cache-dir faster-whisper || true && \
    adduser -u 65532 -D app || true && \
    mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8080/ || exit 1
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="faster-whisper" \
      org.opencontainers.image.description="faster-whisper container image" \
      org.opencontainers.image.version="1.1.1" \
      org.opencontainers.image.vendor="Guillaume" \
      org.opencontainers.image.source="https://github.com/SYSTRAN/faster-whisper" \
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
