# =============================================================================
# SOVEREIGN HARDENED ETCD
# Generated from template - Version: 3.5.15
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=3.5.15
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends etcd ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' etcd 2>/dev/null || true
RUN mkdir -p /app /var/log/etcd /var/cache/etcd && chown -R etcd:etcd /app /var/log/etcd /var/cache/etcd 2>/dev/null || true
USER etcd:etcd
WORKDIR /app
EXPOSE 2379 2380
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD etcdctl endpoint-health
ENTRYPOINT ["etcd"]
LABEL org.opencontainers.image.title="etcd" \
      org.opencontainers.image.version="3.5.15" \
      org.opencontainers.image.vendor="etcd" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
