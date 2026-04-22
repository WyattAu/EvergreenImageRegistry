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

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache ca-certificates
COPY --from=builder /install/bin/ /usr/local/bin/
COPY --from=builder /valkey-${VERSION}/valkey.conf /app/valkey.conf
RUN useradd -m -u 65532 -s /usr/sbin/nologin valkey 2>/dev/null || true && \
    mkdir -p /app /var/log/valkey-cluster /var/cache/valkey-cluster /var/lib/valkey && \
    chown -R 65532:65532 /app /var/log/valkey-cluster /var/cache/valkey-cluster /var/lib/valkey
USER 65532:65532
WORKDIR /app
EXPOSE 6379 16379
ENV VALKEY_CLUSTER_ANNOUNCE_IP="" \
    VALKEY_CLUSTER_ANNOUNCE_PORT="6379"
ENTRYPOINT ["valkey", "--cluster-enabled", "yes", \
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
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM