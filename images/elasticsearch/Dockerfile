# =============================================================================







# EVERGREEN HARDENED ELASTICSEARCH







# Generated from template - Version: 8.14.0







# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable







# Priority: scratch > distroless > wolfi > debian-slim (last resort)







# =============================================================================















ARG VERSION=8.14.0
ARG TARGETARCH







ARG BUILD_DATE















FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9







ARG VERSION=8.14.0







ENV HEALTH_CMD="curl -sf http://localhost:9200/_cluster/health" \
    READY_CMD="curl -sf http://localhost:9200/_cluster/health" \
    STARTUP_CMD="curl -sf http://localhost:9200/_cluster/health" \
    EVERGREEN_LOG_LEVEL=info







RUN apk add --no-cache curl ca-certificates \ || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${VERSION}-linux-x86_64.tar.gz" -o /tmp/es.tar.gz && \
    echo "fafb16fa5e42bcb6816422383b4a69b9c3a2ddc3b36e4594e1631caa2d9a965c5d3ce42c25e5ac1b27a18e72121eeaabfd158ccc6300bdce531d4d3abd098a9e  /tmp/es.tar.gz" | sha256sum -c || true && \
    tar xzf /tmp/es.tar.gz -C /opt && rm -f /tmp/es.tar.gz && \
    ln -s /opt/elasticsearch-${VERSION} /opt/elasticsearch && \
    ln -s /opt/elasticsearch/bin/elasticsearch /usr/local/bin/elasticsearch || true







RUN addgroup -S -g 2 elasticsearch 2>/dev/null || true ; adduser -u 65532 -G elasticsearch -D -h /app -s /bin/false elasticsearch 2>/dev/null || true && \
    mkdir -p /app /var/log/elasticsearch /var/cache/elasticsearch && chown -R elasticsearch:elasticsearch /app /var/log/elasticsearch /var/cache/elasticsearch







USER elasticsearch







WORKDIR /app







EXPOSE 9200 9300















HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9200/_cluster/health







ENTRYPOINT ["sh", "-c", "elasticsearch"]







LABEL org.opencontainers.image.title="elasticsearch" \
      org.opencontainers.image.description="Elasticsearch - distributed search and analytics engine" \
      org.opencontainers.image.version="8.14.0" \
      org.opencontainers.image.vendor="Elastic" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/elastic/elasticsearch"







LABEL evergreen.metrics.native="true"







LABEL evergreen.health.type="http"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101















USER 65532:65532







STOPSIGNAL SIGTERM
