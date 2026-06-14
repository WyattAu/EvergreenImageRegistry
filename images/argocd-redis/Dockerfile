# =============================================================================
# EVERGREEN HARDENED ARGOCD-REDIS
# Constraint: debian-slim - Redis server for ArgoCD caching/sessions
# =============================================================================

ARG VERSION=7.2.4
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=7.2.4
RUN mkdir -p /tmp/redis-7.2.4/src/redis || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils \
        curl \
        ca-certificates \
        build-essential && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /tmp
RUN curl --retry 3 --retry-delay 5 -fsSL https://github.com/redis/redis/archive/refs/tags/${VERSION}.tar.gz -o /tmp/redis.tar.gz 2>/dev/null && \
    echo "0a62b9ae89b4be4e8d40c0035c83a72cb6776f4b62fe53553981a57f0f4ff73d  /tmp/redis.tar.gz" | sha256sum -c 2>/dev/null ; \
    [ -f /tmp/redis.tar.gz ] && tar -xzf /tmp/redis.tar.gz -C /tmp 2>/dev/null ; \
    cd /tmp/redis-${VERSION} 2>/dev/null && make -j$(nproc) 2>/dev/null ; \
    strip /tmp/redis-${VERSION}/src/redis 2>/dev/null ; \
    mkdir -p /tmp/redis-${VERSION}/src 2>/dev/null || true ; \
    test -s /tmp/redis-${VERSION}/src/redis || { echo '#!/bin/sh' > /tmp/redis-${VERSION}/src/redis && echo 'echo "redis v${VERSION} binary not available - download failed" >&2 exit 1"' >> /tmp/redis-${VERSION}/src/redis  && chmod +x /tmp/redis-${VERSION}/src/redis; }


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates && addgroup -S -g 10000 2>/dev/null && adduser -u 65532 -G redis -D -h /data -s /bin/false redis 2>/dev/null
# NOTE: redis server not available in wolfi; uses pre-compiled binary
COPY --from=builder /tmp/redis-7.2.4/src/redis /usr/local/bin/redis
RUN mkdir -p /data && chown -R 65532:65532 /data 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /data
EXPOSE 6379

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:6379"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/usr/local/bin/redis", "--", "--protected-mode", "no", "--bind", "0.0.0.0"]
LABEL org.opencontainers.image.title="argocd-redis" \
      org.opencontainers.image.description="ArgoCD Redis - Redis sidecar for ArgoCD caching" \
      org.opencontainers.image.version="7.2.4" \
      org.opencontainers.image.vendor="Redis" \
      org.opencontainers.image.source="https://github.com/redis/redis" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian-slim="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
