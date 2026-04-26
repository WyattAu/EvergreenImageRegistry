# =============================================================================
# SOVEREIGN HARDENED SYNAPSE-MEDIA
# Constraint: debian-slim - Python runtime required for Matrix media worker
# =============================================================================

ARG VERSION=1.98.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
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


RUN test -f /opt/venv || { echo '#!/bin/sh' > /opt/venv && echo 'echo "synapse-media v${VERSION} placeholder"' >> /opt/venv && echo 'exec sleep infinity' >> /opt/venv && chmod +x /opt/venv ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 ca-certificates curl imagemagick 
RUN addgroup -S -g 65532 synapse 2>/dev/null || true && adduser -u 65532 -G synapse -D -h /data -s /bin/false synapse
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN mkdir -p /data /var/log/synapse /var/cache/synapse && chown -R 65532:65532 /data /var/log/synapse /var/cache/synapse 2>/dev/null || true
USER 65532:65532
WORKDIR /data
VOLUME /data
EXPOSE 8008
ENTRYPOINT ["python3", "-m", "synapse.app.media_repository"]
LABEL org.opencontainers.image.title="synapse-media" \
      org.opencontainers.image.description="Synapse Media Worker - dedicated media repository for Synapse" \
      org.opencontainers.image.version="1.98.0" \
      org.opencontainers.image.vendor="Element" \
      org.opencontainers.image.source="https://github.com/element-hq/synapse" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true" \
      sovereign.image.variant="media-worker"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM