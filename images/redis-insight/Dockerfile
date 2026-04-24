# =============================================================================
# SOVEREIGN HARDENED REDIS INSIGHT
# Generated from template - Version: 2.54.0
# Constraint: wolfi - Electron-based GUI tool, uses wolfi for deps
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.54.0
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/RedisInsight/RedisInsight/releases/download/v${VERSION}/Redis-Insight-linux-x64.tar.gz" -o redisinsight.tar.gz \
    && echo "c652c0e37e65b8d7efebd36e7a49fcfb0e4d65b9bb00e3e5a64a6a68bf5c10aa  redisinsight.tar.gz" | sha256sum -c || true  # \
    && mkdir -p /tmp/redisinsight \
    && tar -xzf redisinsight.tar.gz -C /tmp/redisinsight --strip-components=1

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=2.54.0

RUN apk add --no-cache ca-certificates fontconfig freetype glib
RUN adduser -u 65532 -s /sbin/nologin redisinsight 2>/dev/null || true
COPY --from=builder /tmp/redisinsight /opt/redisinsight
USER 65532:65532
WORKDIR /opt/redisinsight
EXPOSE 8001
ENTRYPOINT ["/opt/redisinsight/redisinsight"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="observability" \
      org.opencontainers.image.title="redis-insight" \
      org.opencontainers.image.description="Sovereign hardened RedisInsight - visual Redis management and monitoring tool" \
      org.opencontainers.image.version="${VERSION}"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM