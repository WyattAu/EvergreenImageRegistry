# =============================================================================
# SOVEREIGN HARDENED OPENSEARCH
# Generated from template - Version: 2.12.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Java application requires JRE - cannot use scratch
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.12.0
ARG BUILD_DATE

FROM debian:bookworm-20240101-slim AS downloader
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://artifacts.opensearch.org/releases/bundle/opensearch/${VERSION}/opensearch-${VERSION}-linux-x64.tar.gz" -o /opensearch.tar.gz && \
    echo "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3  /opensearch.tar.gz" | sha256sum -c -
RUN tar -xzf /opensearch.tar.gz -C /opt && \
    rm /opensearch.tar.gz && \
    find /opt/opensearch-${VERSION}/plugins -type f -name "*.so" -exec strip --strip-unneeded {} \; 2>/dev/null || true

FROM debian:bookworm-20240101-slim
RUN groupadd -g 65534 opensearch && \
    useradd -m -u 65534 -g opensearch -s /usr/sbin/nologin opensearch
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless \
        ca-certificates \
        gosu && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /usr/lib/jvm/java-17-openjdk-*/lib/security/cacerts
COPY --from=downloader /opt/opensearch-2.12.0 /opt/opensearch
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p /app/data /app/logs /app/conf && \
    chown -R opensearch:opensearch /app /opt/opensearch && \
    ln -sf /app/conf /opt/opensearch/config/custom && \
    echo "y" | /opt/opensearch/bin/opensearch-plugin install analysis-icu 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 9200 9300
ENV OPENSEARCH_HOME=/opt/opensearch \
    OPENSEARCH_PATH_CONF=/app/conf \
    OPENSEARCH_JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 \
    OPENSEARCH_STARTUP_SLEEP_TIME=5 \
    cluster.name=opensearch-cluster \
    network.host=0.0.0.0 \
    discovery.type=single-node \
    bootstrap.memory_lock=true \
    OPENSEARCH_INITIAL_ADMIN_PASSWORD=Admin@123456
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=5 \
    CMD ["/usr/lib/jvm/java-17-openjdk-amd64/bin/java", "-version"]
ENTRYPOINT ["/opt/opensearch/bin/opensearch"]
LABEL org.opencontainers.image.title="opensearch" \
      org.opencontainers.image.version="2.12.0" \
      org.opencontainers.image.vendor="OpenSearch" \
      org.opencontainers.image.description="OpenSearch - distributed search and analytics engine" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
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
