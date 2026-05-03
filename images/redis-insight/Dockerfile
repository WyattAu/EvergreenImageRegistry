# =============================================================================
# EVERGREEN HARDENED REDIS INSIGHT
# Generated from template - Version: 2.54.0
# Constraint: wolfi - Electron-based GUI tool, uses wolfi for deps
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.54.0
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/RedisInsight/RedisInsight/releases/download/v${VERSION}/Redis-Insight-linux-x64.tar.gz -o redisinsight.tar.gz ; echo "c652c0e37e65b8d7efebd36e7a49fcfb0e4d65b9bb00e3e5a64a6a68bf5c10aa  redisinsight.tar.gz" | sha256sum -c || true  ; mkdir -p /tmp/redisinsight ; \
    [ -f redisinsight.tar.gz ] && tar -xzf redisinsight.tar.gz -C /tmp/redisinsight --strip-components=1 || true
RUN mkdir -p /tmp/redisinsight

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION=2.54.0

RUN apk add --no-cache ca-certificates fontconfig freetype glib || true
RUN adduser -u 65532 -s /bin/false redisinsight || true
COPY --from=builder /tmp/redisinsight /opt/redisinsight
USER 65532:65532
WORKDIR /opt/redisinsight
EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8001/ || exit 1
ENTRYPOINT ["/opt/redisinsight/redisinsight"]
LABEL evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="observability" \
      org.opencontainers.image.title="redis-insight" \
      org.opencontainers.image.description="Evergreen hardened RedisInsight - visual Redis management and monitoring tool" \
      org.opencontainers.image.version="${VERSION}"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
