# =============================================================================
# EVERGREEN HARDENED PREFECT
# Generated from template - Version: 3.3.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.3.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates curl python3 py3-pip 2>/dev/null || apk add --no-cache ca-certificates curl python3 pip 2>/dev/null || true && \
    pip install --no-cache-dir --break-system-packages prefect 2>/dev/null || \
    pip install --no-cache-dir prefect || true && \
    adduser -u 65532 -D app || true && \
    mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python
USER 65532:65532
WORKDIR /app
EXPOSE 4200

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:4200/ || exit 1
ENTRYPOINT ["prefect"]
LABEL org.opencontainers.image.title="prefect" \
      org.opencontainers.image.description="prefect container image" \
      org.opencontainers.image.version="3.3.0" \
      org.opencontainers.image.vendor="Prefect" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/PrefectHQ/prefect"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
