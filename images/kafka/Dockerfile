# =============================================================================
# SOVEREIGN HARDENED KAFKA
# Generated from template - Version: 4.1.2
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.1.2
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://downloads.apache.org/kafka/${VERSION}/kafka_2.13-${VERSION}.tgz" -o /tmp/kafka.tgz && \
    tar -xzf /tmp/kafka.tgz -C /opt && mv /opt/kafka_2.13-${VERSION} /opt/kafka && rm /tmp/kafka.tgz
RUN useradd -m -u 65534 -g '' kafka 2>/dev/null || true
RUN mkdir -p /app /var/log/kafka /var/cache/kafka && chown -R kafka:kafka /app /var/log/kafka /var/cache/kafka /opt/kafka 2>/dev/null || true
USER kafka
WORKDIR /app
EXPOSE 9092
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /opt/kafka/bin/kafka-broker-api-versions.sh --bootstrap-server localhost:9092 2>/dev/null || exit 1
ENTRYPOINT ["/opt/kafka/bin/kafka-server-start.sh", "/opt/kafka/config/server.properties"]
LABEL org.opencontainers.image.title="kafka" \
      org.opencontainers.image.version="4.1.2" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
