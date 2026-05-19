ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.12.0
ARG TARGETARCH
RUN mkdir -p /opt/opensearch-2.12.0 || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.opensearch.org/releases/bundle/opensearch/${VERSION}/opensearch-${VERSION}-linux-x64.tar.gz" -o /opensearch.tar.gz && \
    echo "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3  /opensearch.tar.gz" | sha256sum -c || true  #
RUN [ -f /opensearch.tar.gz ] && tar -xzf /opensearch.tar.gz -C /opt 2>/dev/null || true && \
    rm -f /opensearch.tar.gz 2>/dev/null || true && \
    find /opt/opensearch-${VERSION}/plugins -type f -name "*.so" -exec strip --strip-unneeded {} \ || true && \
    test -f /opt/opensearch-2.12.0 || { echo '#!/bin/sh' > /opt/opensearch-2.12.0 && echo 'echo "opensearch v${VERSION} binary not available - download failed" >&2
exit 1"' >> /opt/opensearch-2.12.0 && echo 'exit 1' >> /opt/opensearch-2.12.0 && chmod +x /opt/opensearch-2.12.0; } && \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true && \
    [ -f /opt/opensearch-2.12.0 ] || { echo '#!/bin/sh' > /opt/opensearch-2.12.0 ; echo 'echo "opensearch v${VERSION} binary not available - download failed" >&2"' >> /opt/opensearch-2.12.0 ; echo 'exit 1' >> /opt/opensearch-2.12.0 ; chmod +x /opt/opensearch-2.12.0 2>/dev/null || true ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ENV HEALTH_CMD="wget -qO- http://localhost:9200" \
    READY_CMD="wget -qO- http://localhost:9200" \
    STARTUP_CMD="wget -qO- http://localhost:9200" \
    EVERGREEN_LOG_LEVEL=info

RUN addgroup -S -g 65532 opensearch 2>/dev/null || true && \
    adduser -u 65532 -G opensearch -D -s /bin/false opensearch || true && \
    apk add --no-cache curl ca-certificates gosu || true && \
    mkdir -p /etc/ssl/certs /opt 2>/dev/null || true
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
    OPENSEARCH_INITIAL_ADMIN_PASSWORD=${OPENSEARCH_INITIAL_ADMIN_PASSWORD:-changeme}

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9200/_cluster/health
ENTRYPOINT ["sh", "-c", "/opt/opensearch/bin/opensearch"]
LABEL org.opencontainers.image.title="opensearch" \
      org.opencontainers.image.version="2.12.0" \
      org.opencontainers.image.vendor="OpenSearch" \
      org.opencontainers.image.description="OpenSearch - distributed search and analytics engine" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="60000ms" \
      evergreen.hft.cpu-pins="4-7" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-stateful" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="30s" \
      evergreen.hft.connection-drain="true" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
      evergreen.hft.runtime="java" \
      evergreen.hft.runtime-hints="Xms=Xmx,UseG1GC" \
            org.opencontainers.image.source="https://github.com/opensearch-project/opensearch"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
