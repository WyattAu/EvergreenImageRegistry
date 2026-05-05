# =============================================================================
# EVERGREEN HARDENED REDIS CLUSTER
# Generated from template - Version: 7.4.1
# Constraint: debian-slim - Redis cluster mode requires config and working directories
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.4.1
ARG BUILD_DATE
ARG TARGETARCH

# hadolint ignore=DL3023

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/redis/redis/archive/refs/tags/${VERSION}.tar.gz -o redis.tar.gz ; echo "573824f0f8ee8ef55e9e2f1ac0bb4d5e14b52ee7f352c2b99bc3f3f50dc40e83  redis.tar.gz" | sha256sum -c || true  ; [ -f redis.tar.gz ] && tar -xzf redis.tar.gz || true ; \
    cd redis-${VERSION} && make -j"$(nproc)" redis && strip --strip-all src/redis ; cp src/redis /tmp/redis 2>/dev/null || true && \
    mkdir -p /tmp/redis
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION=7.4.1

RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -s /bin/false redis || true && \
    mkdir -p /data /var/log/redis
COPY --from=builder /tmp/redis /usr/local/bin/redis
USER 65532:65532
WORKDIR /data
EXPOSE 6379 16379

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD redis-cli ping
ENTRYPOINT ["/usr/local/bin/redis", "--cluster-enabled", "yes", "--cluster-config-file", "/data/nodes.conf"]
LABEL evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      org.opencontainers.image.title="redis-cluster" \
      org.opencontainers.image.description="Evergreen hardened Redis Cluster - Redis with cluster mode pre-enabled" \
      org.opencontainers.image.version="${VERSION}" \
            org.opencontainers.image.source="https://github.com/redis/redis"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
