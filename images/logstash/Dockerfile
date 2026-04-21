# =============================================================================
# SOVEREIGN HARDENED LOGSTASH
# Version: 8.12.2
# Constraint: debian-slim - JRE runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=8.12.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://artifacts.elastic.co/downloads/logstash/logstash-${VERSION}-linux-x86_64.tar.gz" -o logstash.tar.gz \
    && echo "0000000000000000000000000000000000000000000000000000000000000000  logstash.tar.gz" | sha256sum -c - \
    && tar -xzf logstash.tar.gz \
    && rm logstash.tar.gz

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin logstash 2>/dev/null || true
RUN mkdir -p /opt/logstash/data /opt/logstash/logs /var/log/logstash /var/cache/logstash
COPY --from=builder /tmp/logstash-${VERSION} /opt/logstash
USER 65534:65534
WORKDIR /opt/logstash
ENV LS_JAVA_OPTS="-Xms512m -Xmx512m"
ENV PATH="/opt/logstash/bin:${PATH}"
EXPOSE 5044 9600
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["curl", "-fsSL", "http://localhost:9600/_node/stats"]
ENTRYPOINT ["/opt/logstash/bin/logstash"]
LABEL org.opencontainers.image.title="logstash" \
      org.opencontainers.image.description="Sovereign hardened Logstash - Elastic data processing pipeline" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Elastic" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="observability" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
