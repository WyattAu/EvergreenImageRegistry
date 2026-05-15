# =============================================================================
# EVERGREEN HARDENED INVOKEAI
# Generated from template - Version: 5.5.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.5.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates curl && \
    pip install --no-cache-dir --break-system-packages invokeai 2>/dev/null || \
    pip install --no-cache-dir invokeai || true && \
    adduser -u 65532 -D app 2>/dev/null || true && \
    mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 9090

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9090/ || exit 1
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="invokeai" \
      org.opencontainers.image.description="invokeai container image" \
      org.opencontainers.image.version="5.5.0" \
      org.opencontainers.image.vendor="InvokeAI" \
      org.opencontainers.image.source="https://github.com/invoke-ai/InvokeAI" \
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
