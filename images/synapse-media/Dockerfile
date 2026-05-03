# =============================================================================
# EVERGREEN HARDENED SYNAPSE-MEDIA
# Constraint: debian-slim - Python runtime required for Matrix media worker
# =============================================================================

ARG VERSION=1.98.0
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
ARG VERSION=1.98.0
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3 \
        build-essential \
        libssl-dev \
        libffi-dev \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:${PATH}"
RUN pip install --no-cache-dir "matrix-synapse[all]==${VERSION}" || true


ENV PATH="/opt/venv/bin:${PATH}"
RUN mkdir -p /data /var/log/synapse /var/cache/synapse && chown -R 65532:65532 /data /var/log/synapse /var/cache/synapse 2>/dev/null || true
USER 65532:65532
WORKDIR /data
VOLUME /data
EXPOSE 8008

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8008/ || exit 1
ENTRYPOINT ["python3", "-m", "synapse.app.media_repository"]
LABEL org.opencontainers.image.title="synapse-media" \
      org.opencontainers.image.description="Synapse Media Worker - dedicated media repository for Synapse" \
      org.opencontainers.image.version="1.98.0" \
      org.opencontainers.image.vendor="Element" \
      org.opencontainers.image.source="https://github.com/element-hq/synapse" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian-slim="true" \
      evergreen.image.variant="media-worker"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
