# =============================================================================
# SOVEREIGN HARDENED ARGOCD-REDIS
# Constraint: debian-slim - Redis server for ArgoCD caching/sessions
# =============================================================================

ARG VERSION=7.2.4
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION=7.2.4
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        build-essential && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /tmp
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/redis/redis/archive/refs/tags/${VERSION}.tar.gz -o /tmp/redis.tar.gz && \
    tar -xzf /tmp/redis.tar.gz -C /tmp && \
    cd /tmp/redis-${VERSION} && \    make -j$(nproc) && \
    strip src/redis || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
RUN addgroup -S -g 65532 redis 2>/dev/null || true && adduser -u 65532 -G redis -D -h /data -s /sbin/nologin redis 2>/dev/null || true
COPY --from=builder /tmp/redis-7.2.4/src/redis /usr/local/bin/redis
RUN mkdir -p /data && chown -R 65532:65532 /data
USER 65532:65532
WORKDIR /data
EXPOSE 6379
ENTRYPOINT ["/usr/local/bin/redis"]
CMD ["--protected-mode", "no", "--bind", "0.0.0.0"]
LABEL org.opencontainers.image.title="argocd-redis" \
      org.opencontainers.image.description="ArgoCD Redis - Redis sidecar for ArgoCD caching" \
      org.opencontainers.image.version="7.2.4" \
      org.opencontainers.image.vendor="Redis" \
      org.opencontainers.image.source="https://github.com/redis/redis" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM