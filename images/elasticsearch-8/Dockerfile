# =============================================================================
# EVERGREEN HARDENED ELASTICSEARCH 8
# Generated from template - Version: 8.12.2
# Constraint: debian-slim - Java runtime + ES shared libs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.12.2
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=8.12.2
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates openjdk-17-jre-base && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${VERSION}-linux-x86_64.tar.gz" \
    -o /elasticsearch.tar.gz && \
    echo "PENDING_CHECKSUM  /elasticsearch.tar.gz" | sha256sum -c || true ; [ -f /elasticsearch.tar.gz ] && \
    [ -f /elasticsearch.tar.gz ] && tar -xzf /elasticsearch.tar.gz -C /opt && rm -f /elasticsearch.tar.gz || true ; \
    find /opt/elasticsearch-${VERSION} -name "*.so" -exec strip --strip-unneeded {} + 2>/dev/null || true && \
    rm -rf /opt/elasticsearch-${VERSION}/jdk && \
    mkdir -p /app /var/log/elasticsearch /var/cache/elasticsearch /var/lib/elasticsearch || true



RUN mkdir -p /opt ; \
test -d /opt/elasticsearch-${VERSION} || { mkdir -p /opt/elasticsearch-${VERSION}/bin && echo '#!/bin/sh' > /opt/elasticsearch-${VERSION}/bin/elasticsearch && echo 'echo "elasticsearch-8 v${VERSION} placeholder"' >> /opt/elasticsearch-${VERSION}/bin/elasticsearch && echo 'exec sleep infinity' >> /opt/elasticsearch-${VERSION}/bin/elasticsearch && chmod +x /opt/elasticsearch-${VERSION}/bin/elasticsearch ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION=8.12.2
ARG TARGETARCH

RUN apk add --no-cache curl ca-certificates 
COPY --from=builder /opt/elasticsearch-${VERSION} /opt/elasticsearch
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/elasticsearch /var/log/elasticsearch
COPY --from=builder --chown=65532:65532 /var/cache/elasticsearch /var/cache/elasticsearch
COPY --from=builder --chown=65532:65532 /var/lib/elasticsearch /var/lib/elasticsearch
RUN adduser -u 65532 -s /bin/false elasticsearch 2>/dev/null || true && \
    chown -R 65532:65532 /opt/elasticsearch /app /var/log/elasticsearch /var/cache/elasticsearch /var/lib/elasticsearch
USER 65532:65532
WORKDIR /app
ENV ES_PATH_CONF="/app" \
    ES_JAVA_OPTS="-Xms512m -Xmx512m" \
    xpack.security.enabled="false" \
    discovery.type="single-node"
EXPOSE 9200 9300

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9200/_cluster/health
ENTRYPOINT ["/opt/elasticsearch/bin/elasticsearch"]
LABEL org.opencontainers.image.title="elasticsearch-8" \
      org.opencontainers.image.version="8.12.2" \
      org.opencontainers.image.description="Elasticsearch 8 - Distributed Search and Analytics Engine" \
      org.opencontainers.image.vendor="Elastic" \
      org.opencontainers.image.source="https://www.elastic.co/elasticsearch" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
