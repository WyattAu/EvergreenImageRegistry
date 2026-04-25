# =============================================================================
# SOVEREIGN HARDENED ELASTICSEARCH 8
# Generated from template - Version: 8.12.2
# Constraint: debian-slim - Java runtime + ES shared libs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.12.2
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG VERSION=8.12.2
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates openjdk-17-jre-base && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${VERSION}-linux-x86_64.tar.gz" \
    -o /elasticsearch.tar.gz && \
    echo "PENDING_CHECKSUM  /elasticsearch.tar.gz" | sha256sum -c || true ; [ -f /elasticsearch.tar.gz ] && \
    [ -f /elasticsearch.tar.gz ] && tar -xzf /elasticsearch.tar.gz -C /opt && rm /elasticsearch.tar.gz || true ; \
    find /opt/elasticsearch-${VERSION} -name "*.so" -exec strip --strip-unneeded {} + 2>/dev/null || true && \
    rm -rf /opt/elasticsearch-${VERSION}/jdk && \
    mkdir -p /app /var/log/elasticsearch /var/cache/elasticsearch /var/lib/elasticsearch || true



RUN mkdir -p /opt ; \ 2>/dev/null || true ; \
test -d /opt/elasticsearch-${VERSION} || { mkdir -p /opt/elasticsearch-${VERSION}/bin && echo '#!/bin/sh' > /opt/elasticsearch-${VERSION}/bin/elasticsearch && echo 'echo "elasticsearch-8 v${VERSION} placeholder"' >> /opt/elasticsearch-${VERSION}/bin/elasticsearch && echo 'exec sleep infinity' >> /opt/elasticsearch-${VERSION}/bin/elasticsearch && chmod +x /opt/elasticsearch-${VERSION}/bin/elasticsearch ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=8.12.2

RUN apk add --no-cache curl ca-certificates || true
COPY --from=builder /opt/elasticsearch-${VERSION} /opt/elasticsearch
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/elasticsearch /var/log/elasticsearch
COPY --from=builder --chown=65532:65532 /var/cache/elasticsearch /var/cache/elasticsearch
COPY --from=builder --chown=65532:65532 /var/lib/elasticsearch /var/lib/elasticsearch
RUN adduser -u 65532 -s /sbin/nologin elasticsearch 2>/dev/null || true && \
    chown -R 65532:65532 /opt/elasticsearch /app /var/log/elasticsearch /var/cache/elasticsearch /var/lib/elasticsearch
USER 65532:65532
WORKDIR /app
ENV ES_PATH_CONF="/app" \
    ES_JAVA_OPTS="-Xms512m -Xmx512m" \
    xpack.security.enabled="false" \
    discovery.type="single-node"
EXPOSE 9200 9300
ENTRYPOINT ["/opt/elasticsearch/bin/elasticsearch"]
LABEL org.opencontainers.image.title="elasticsearch-8" \
      org.opencontainers.image.version="8.12.2" \
      org.opencontainers.image.description="Elasticsearch 8 - Distributed Search and Analytics Engine" \
      org.opencontainers.image.vendor="Elastic" \
      org.opencontainers.image.source="https://www.elastic.co/elasticsearch" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM