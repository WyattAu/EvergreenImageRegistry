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
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/RedisInsight/RedisInsight/releases/download/v${VERSION}/Redis-Insight-linux-x64.tar.gz" -o redisinsight.tar.gz \
    && echo "c652c0e37e65b8d7efebd36e7a49fcfb0e4d65b9bb00e3e5a64a6a68bf5c10aa  redisinsight.tar.gz" | sha256sum -c - \
    && mkdir -p /tmp/redisinsight \
    && tar -xzf redisinsight.tar.gz -C /tmp/redisinsight --strip-components=1

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates libx11-6 libxext6 libxrender1 libxtst6 libxi6 \
    libfontconfig1 libfreetype6 libglib2.0-0 libnss3 libnspr4 \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 libdbus-1-3 libdrm2 \
    libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin redisinsight 2>/dev/null || true
COPY --from=builder /tmp/redisinsight /opt/redisinsight
USER 65534:65534
WORKDIR /opt/redisinsight
EXPOSE 8001
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["/opt/redisinsight/redisinsight", "--version"]
ENTRYPOINT ["/opt/redisinsight/redisinsight"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="observability" \
      org.opencontainers.image.title="redis-insight" \
      org.opencontainers.image.description="Sovereign hardened RedisInsight - visual Redis management and monitoring tool" \
      org.opencontainers.image.version="${VERSION}"
