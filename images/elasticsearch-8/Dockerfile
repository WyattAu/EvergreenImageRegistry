# =============================================================================
# SOVEREIGN HARDENED ELASTICSEARCH 8
# Generated from template - Version: 8.12.2
# Constraint: debian-slim - Java runtime + ES shared libs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.12.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates openjdk-17-jre-headless && \
    curl -fsSL "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${VERSION}-linux-x86_64.tar.gz" \
    -o /elasticsearch.tar.gz && \
    echo "PENDING_CHECKSUM  /elasticsearch.tar.gz" | sha256sum -c - && \
    tar -xzf /elasticsearch.tar.gz -C /opt && rm /elasticsearch.tar.gz && \
    find /opt/elasticsearch-${VERSION} -name "*.so" -exec strip --strip-unneeded {} + 2>/dev/null || true && \
    rm -rf /opt/elasticsearch-${VERSION}/jdk && \
    mkdir -p /app /var/log/elasticsearch /var/cache/elasticsearch /var/lib/elasticsearch

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder /opt/elasticsearch-${VERSION} /opt/elasticsearch
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /var/log/elasticsearch /var/log/elasticsearch
COPY --from=builder --chown=65534:65534 /var/cache/elasticsearch /var/cache/elasticsearch
COPY --from=builder --chown=65534:65534 /var/lib/elasticsearch /var/lib/elasticsearch
RUN useradd -m -u 65534 -s /usr/sbin/nologin elasticsearch 2>/dev/null || true && \
    chown -R 65534:65534 /opt/elasticsearch /app /var/log/elasticsearch /var/cache/elasticsearch /var/lib/elasticsearch
USER 65534:65534
WORKDIR /app
ENV ES_PATH_CONF="/app" \
    ES_JAVA_OPTS="-Xms512m -Xmx512m" \
    xpack.security.enabled="false" \
    discovery.type="single-node"
EXPOSE 9200 9300
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=5 \
    CMD ["curl", "-f", "http://localhost:9200/_cluster/health"]
ENTRYPOINT ["/opt/elasticsearch/bin/elasticsearch"]
LABEL org.opencontainers.image.title="elasticsearch-8" \
      org.opencontainers.image.version="8.12.2" \
      org.opencontainers.image.description="Elasticsearch 8 - Distributed Search and Analytics Engine" \
      org.opencontainers.image.vendor="Elastic" \
      org.opencontainers.image.source="https://www.elastic.co/elasticsearch" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
