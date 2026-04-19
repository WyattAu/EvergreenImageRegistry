# =============================================================================
# SOVEREIGN HARDENED ETCD
# Generated from template - Version: 3.5.15
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=3.5.15
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:3.5.15
RUN apk add --no-cache etcd ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 etcd 2>/dev/null || true
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
      sovereign.constraint.wolfi="true"
