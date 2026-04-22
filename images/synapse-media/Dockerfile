# =============================================================================
# SOVEREIGN HARDENED SYNAPSE-MEDIA
# Constraint: debian-slim - Python runtime required for Matrix media worker
# =============================================================================

ARG VERSION=1.98.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3="3.11.*" \
        py3-pip="23.1.*" \
        python3="3.11.*" \
        build-base \
        libssl-dev \
        libffi-dev \
        curl="7.88.1-*" \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN pip install --no-cache-dir "matrix-synapse[all]==${VERSION}"

FROM cgr.dev/chainguard/wolfi-base:latest

SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apk add --no-cache python3 ca-certificates curl imagemagick
RUN groupadd -r -g 65532 synapse && useradd -r -u 65532 -g synapse -d /data -s /usr/sbin/nologin synapse
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN mkdir -p /data /var/log/synapse /var/cache/synapse && chown -R 65532:65532 /data /var/log/synapse /var/cache/synapse
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