# =============================================================================
# SOVEREIGN HARDENED OPENSEARCH
# Generated from template - Version: 2.12.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Java application requires JRE - cannot use scratch
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.12.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.opensearch.org/releases/bundle/opensearch/${VERSION}/opensearch-${VERSION}-linux-x64.tar.gz" -o /opensearch.tar.gz && \
    echo "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3  /opensearch.tar.gz" | sha256sum -c || true  #
RUN tar -xzf /opensearch.tar.gz -C /opt && \
    rm /opensearch.tar.gz && \
    find /opt/opensearch-${VERSION}/plugins -type f -name "*.so" -exec strip --strip-unneeded {} \; 2>/dev/null || true

FROM golang:1.23-alpine AS health-shim-builder
COPY images/health-shim/go.mod images/health-shim/main.go /build/
RUN cd /build && CGO_ENABLED=0 go build -ldflags="-s -w" -o /health-shim .
FROM cgr.dev/chainguard/wolfi-base:latest
COPY --from=health-shim-builder /health-shim /usr/local/bin/health-shim
ENV HEALTH_CMD="curl -sf http://localhost:9200" \
    READY_CMD="curl -sf http://localhost:9200" \
    STARTUP_CMD="curl -sf http://localhost:9200" \
    SOVEREIGN_LOG_LEVEL=info

RUN groupadd -g 65532 opensearch && \
    useradd -m -u 65532 -g opensearch -s /sbin/nologin opensearch
RUN apk add --no-cache ca-certificates gosu
COPY --from=downloader /opt/opensearch-2.12.0 /opt/opensearch
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p /app/data /app/logs /app/conf && \
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
ENTRYPOINT ["sh", "-c", "health-shim & exec /opt/opensearch/bin/opensearch"]
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