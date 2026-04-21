# =============================================================================
# SOVEREIGN HARDENED VALKEY CLUSTER
# Generated from template - Version: 7.2.4
# Constraint: debian-slim - Valkey cluster mode with redis-trib
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=7.2.4
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/valkey-io/valkey/releases/download/${VERSION}/valkey-${VERSION}.tar.gz" \
    -o /valkey.tar.gz && \
    echo "PENDING_CHECKSUM  /valkey.tar.gz" | sha256sum -c - && \
    tar -xzf /valkey.tar.gz -C / && rm /valkey.tar.gz && \
    cd /valkey-${VERSION} && make -j"$(nproc)" && make install PREFIX=/install && \
    strip /install/bin/valkey-* /install/bin/redis-*

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder /install/bin/ /usr/local/bin/
COPY --from=builder /valkey-${VERSION}/valkey.conf /app/valkey.conf
RUN useradd -m -u 65534 -s /usr/sbin/nologin valkey 2>/dev/null || true && \
    mkdir -p /app /var/log/valkey-cluster /var/cache/valkey-cluster /var/lib/valkey && \
    chown -R 65534:65534 /app /var/log/valkey-cluster /var/cache/valkey-cluster /var/lib/valkey
USER 65534:65534
WORKDIR /app
EXPOSE 6379 16379
ENV VALKEY_CLUSTER_ANNOUNCE_IP="" \
    VALKEY_CLUSTER_ANNOUNCE_PORT="6379"
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["valkey-cli", "-p", "6379", "ping"]
ENTRYPOINT ["valkey-server", "--cluster-enabled", "yes", \
    "--cluster-config-file", "/app/nodes.conf", \
    "--cluster-node-timeout", "5000", \
    "--appendonly", "yes", \
    "--port", "6379"]
LABEL org.opencontainers.image.title="valkey-cluster" \
      org.opencontainers.image.version="7.2.4" \
      org.opencontainers.image.description="Valkey in Cluster Mode - Distributed Key-Value Store" \
      org.opencontainers.image.vendor="Valkey" \
      org.opencontainers.image.source="https://github.com/valkey-io/valkey" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
