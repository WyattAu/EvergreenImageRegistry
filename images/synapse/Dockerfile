# =============================================================================
# SOVEREIGN HARDENED SYNAPSE
# Constraint: debian-slim - Python runtime required for Matrix homeserver
# =============================================================================

ARG VERSION=1.98.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3="3.11.*" \
        python3-pip="23.1.*" \
        python3-venv="3.11.*" \
        build-essential \
        libssl-dev \
        libffi-dev \
        curl="7.88.1-*" \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN pip install --no-cache-dir "matrix-synapse[all]==${VERSION}"

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3="3.11.*" \
        ca-certificates \
        curl="7.88.1-*" && \
    rm -rf /var/lib/apt/lists/*
RUN groupadd -r -g 65534 synapse && useradd -r -u 65534 -g synapse -d /data -s /usr/sbin/nologin synapse
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN mkdir -p /data /var/log/synapse /var/cache/synapse && chown -R 65534:65534 /data /var/log/synapse /var/cache/synapse
USER 65534:65534
WORKDIR /data
VOLUME /data
EXPOSE 8008 8448
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:8008/_matrix/client/versions"]
ENTRYPOINT ["python3", "-m", "synapse.app.homeserver"]
LABEL org.opencontainers.image.title="synapse" \
      org.opencontainers.image.description="Synapse - Matrix homeserver for federated messaging" \
      org.opencontainers.image.version="1.98.0" \
      org.opencontainers.image.vendor="Element" \
      org.opencontainers.image.source="https://github.com/element-hq/synapse" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true"
