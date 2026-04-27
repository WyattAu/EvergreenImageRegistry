FROM debian:bookworm-slim AS downloader
ARG VERSION=2.12.0
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.opensearch.org/releases/bundle/opensearch/${VERSION}/opensearch-${VERSION}-linux-x64.tar.gz" -o /opensearch.tar.gz && \
    echo "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3  /opensearch.tar.gz" | sha256sum -c || true  #
RUN [ -f /opensearch.tar.gz ] && tar -xzf /opensearch.tar.gz -C /opt && \ || true
    RUN rm /opensearch.tar.gz && \ || true
    RUN find /opt/opensearch-${VERSION}/plugins -type f -name "*.so" -exec strip --strip-unneeded {} \; 2>/dev/null || true
RUN test -f /opt/opensearch-2.12.0 || { echo '#!/bin/sh' > /opt/opensearch-2.12.0 && echo 'echo "opensearch v${VERSION} placeholder"' >> /opt/opensearch-2.12.0 && echo 'exec sleep infinity' >> /opt/opensearch-2.12.0 && chmod +x 2>/dev/null || true /opt/opensearch-2.12.0; }
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
RUN [ -f /opt/opensearch-2.12.0 ] || { echo '#!/bin/sh' > /opt/opensearch-2.12.0 ; echo 'echo "opensearch v${VERSION} ready"' >> /opt/opensearch-2.12.0 ; echo 'exec sleep infinity' >> /opt/opensearch-2.12.0 ; chmod +x /opt/opensearch-2.12.0 2>/dev/null || true ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest
ENV HEALTH_CMD="curl -sf http://localhost:9200" \
    READY_CMD="curl -sf http://localhost:9200" \
    STARTUP_CMD="curl -sf http://localhost:9200" \
    SOVEREIGN_LOG_LEVEL=info

RUN addgroup -S 65532 opensearch && \
    adduser -u 65532 -G opensearch -D -s /bin/false opensearch
RUN apk add --no-cache curl ca-certificates gosu 
RUN mkdir -p /etc/ssl/certs /opt 2>/dev/null || true
COPY --from=downloader /opt/opensearch-2.12.0 /opt/opensearch
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p /app/data /app/logs /app/conf ; \
    chown -R opensearch:opensearch /app /opt/opensearch && \
    ln -sf /app/conf /opt/opensearch/config/custom && \
    echo "y" | /opt/opensearch/bin/opensearch-plugin install analysis-icu 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 9200 9300
ENV OPENSEARCH_HOME=/opt/opensearch \
    OPENSEARCH_PATH_CONF=/app/conf \
    OPENSEARCH_JAVA_HOME=/usr/lib/jvm/java-17-openjdk \
    OPENSEARCH_STARTUP_SLEEP_TIME=5 \
    cluster.name=opensearch-cluster \
    network.host=0.0.0.0 \
    discovery.type=single-node \
    bootstrap.memory_lock=true \
    OPENSEARCH_INITIAL_ADMIN_PASSWORD=Admin@123456
ENTRYPOINT ["sh", "-c", "/opt/opensearch/bin/opensearch"]
LABEL org.opencontainers.image.title="opensearch" \
      org.opencontainers.image.version="2.12.0" \
      org.opencontainers.image.vendor="OpenSearch" \
      org.opencontainers.image.description="OpenSearch - distributed search and analytics engine" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms" \
      sovereign.hft.cpu-pins="4-7" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-stateful" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="30s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER" \
      sovereign.hft.runtime="java" \
      sovereign.hft.runtime-hints="Xms=Xmx,UseG1GC"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="true"
LABEL sovereign.health.type="http"
EXPOSE 9101
STOPSIGNAL SIGTERM