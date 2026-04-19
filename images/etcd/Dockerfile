# =============================================================================
# SOVEREIGN HARDENED ETCD
# Generated from template - Version: 3.5.15
# =============================================================================

ARG VERSION=3.5.15
ARG BUILD_DATE

FROM alpine:3.5.15-alpine
RUN apk add --no-cache etcd ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id etcd 2>/dev/null || adduser -D -u 65534 etcd
RUN mkdir -p /app /var/log/etcd /var/cache/etcd && chown -R etcd:etcd /app /var/log/etcd /var/cache/etcd
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
      sovereign.constraint.nonroot="true"
