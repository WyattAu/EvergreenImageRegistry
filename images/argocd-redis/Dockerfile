# =============================================================================
# SOVEREIGN HARDENED ARGOCD-REDIS
# Constraint: debian-slim - Redis server for ArgoCD caching/sessions
# =============================================================================

ARG VERSION=7.2.4
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl="7.88.1-*" \
        ca-certificates \
        build-essential && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /tmp
RUN curl -fsSL "https://github.com/redis/redis/archive/refs/tags/${VERSION}.tar.gz" -o /tmp/redis.tar.gz && \
    tar -xzf /tmp/redis.tar.gz -C /tmp && \
    cd /tmp/redis-${VERSION} && \
    make -j$(nproc) && \
    strip src/redis-server

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN groupadd -r -g 65534 redis && useradd -r -u 65534 -g redis -d /data -s /usr/sbin/nologin redis
COPY --from=builder /tmp/redis-7.2.4/src/redis-server /usr/local/bin/redis-server
RUN mkdir -p /data && chown -R 65534:65534 /data
USER 65534:65534
WORKDIR /data
EXPOSE 6379
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/redis-server", "--version"]
ENTRYPOINT ["/usr/local/bin/redis-server"]
CMD ["--protected-mode", "no", "--bind", "0.0.0.0"]
LABEL org.opencontainers.image.title="argocd-redis" \
      org.opencontainers.image.description="ArgoCD Redis - Redis sidecar for ArgoCD caching" \
      org.opencontainers.image.version="7.2.4" \
      org.opencontainers.image.vendor="Redis" \
      org.opencontainers.image.source="https://github.com/redis/redis" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true"
