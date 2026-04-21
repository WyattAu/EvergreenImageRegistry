# =============================================================================
# SOVEREIGN HARDENED KAFKA-MANAGER (CMAK)
# Version: 3.0.0.6
# Constraint: debian-slim - JRE runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.0.0.6
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/yahoo/CMAK/releases/download/${VERSION}/cmak-${VERSION}.zip" -o cmak.zip \
    && echo "0000000000000000000000000000000000000000000000000000000000000000  cmak.zip" | sha256sum -c - \
    && apt-get install -y --no-install-recommends unzip \
    && unzip cmak.zip -d /opt/cmak \
    && rm cmak.zip \
    && rm -rf /var/lib/apt/lists/*

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin cmak 2>/dev/null || true
RUN mkdir -p /opt/cmak/logs /var/log/cmak /var/cache/cmak
COPY --from=builder /opt/cmak /opt/cmak
USER 65534:65534
WORKDIR /opt/cmak
EXPOSE 9000
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["curl", "-fsSL", "http://localhost:9000/api/health"]
ENTRYPOINT ["/opt/cmak/bin/cmak"]
LABEL org.opencontainers.image.title="kafka-manager" \
      org.opencontainers.image.description="Sovereign hardened CMAK (Kafka Manager) - Apache Kafka management tool" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Yahoo" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="messaging" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
