# =============================================================================
# SOVEREIGN HARDENED HIVE-METASTORE
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.0.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://archive.apache.org/dist/hive/hive-${VERSION}/apache-hive-${VERSION}-bin.tar.gz" -o /tmp/hive.tar.gz \
    && echo "PENDING  /tmp/hive.tar.gz" | sha256sum -c - \
    && tar -xzf /tmp/hive.tar.gz -C /opt \
    && rm /tmp/hive.tar.gz

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates openjdk-17-jre-headless curl && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin hive 2>/dev/null || true
RUN mkdir -p /var/lib/hive /var/log/hive /var/cache/hive /opt/hive/conf
COPY --from=builder /opt/apache-hive-${VERSION}-bin /opt/hive
RUN chown -R 65534:65534 /opt/hive /var/lib/hive /var/log/hive /var/cache/hive
USER 65534:65534
WORKDIR /opt/hive
EXPOSE 9083
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["curl", "-f", "http://localhost:9083/"]
ENTRYPOINT ["/opt/hive/bin/hive", "--service", "metastore"]
LABEL org.opencontainers.image.title="hive-metastore" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Hive Metastore - metadata service for Apache Hive" \
      org.opencontainers.image.vendor="Apache Software Foundation" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
