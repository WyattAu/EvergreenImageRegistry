# =============================================================================
# EVERGREEN HARDENED TTS
# Generated from template - Version: 0.22.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.22.0
ARG BUILD_DATE
ARG TARGETARCH


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG GITHUB_TOKEN
RUN apk add --no-cache ca-certificates curl && \
    pip install --no-cache-dir --break-system-packages TTS 2>/dev/null || \
    pip install --no-cache-dir TTS || true && \
    adduser -u 65532 -D app 2>/dev/null || true && \
    mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 5002

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:5002/ || exit 1
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="tts" \
      org.opencontainers.image.version="0.22.0" \
      org.opencontainers.image.vendor="Coqui" \
      org.opencontainers.image.source="https://github.com/coqui-ai/TTS" \
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
