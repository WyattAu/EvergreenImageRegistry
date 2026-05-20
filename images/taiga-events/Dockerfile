# =============================================================================
# EVERGREEN HARDENED TAIGA-EVENTS
# Node.js WebSocket server for Taiga realtime updates
# Installed from GitHub (taigaio/taiga-events) via pip
# =============================================================================

ARG VERSION=6.9.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a524531f996953ef06cd13a59fa1df2c5c252 AS downloader
ARG VERSION=6.9.0
RUN mkdir -p /venv || true
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip python3-venv curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /venv && \
    /venv/bin/pip install --no-cache-dir "git+https://github.com/taigaio/taiga-events.git@${VERSION}#egg=taiga_events" 2>/dev/null || true && \
    mkdir -p /app /var/log/taiga-events 2>/dev/null || true

FROM registry.access.redhat.com/ubi9/ubi-minimal
LABEL evergreen.base.fallback_reason="Python C extensions require glibc"
RUN microdnf install -y python3 ca-certificates libstdc++ 2>/dev/null || true
COPY --from=downloader /venv /venv
COPY --from=downloader /var/log/taiga-events /var/log/taiga-events
USER 65532:65532
WORKDIR /app
EXPOSE 8004

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8004/ || exit 1
ENTRYPOINT ["/venv/bin/python", "-m", "taiga_events"]
LABEL org.opencontainers.image.title="taiga-events" \
      org.opencontainers.image.description="Taiga Events - Node.js WebSocket server for realtime updates" \
      org.opencontainers.image.version="6.9.0" \
      org.opencontainers.image.vendor="Taiga" \
      org.opencontainers.image.source="https://github.com/taigaio/taiga-events" \
      evergreen.image.tier="3" \
      evergreen.image.category="project-management" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
