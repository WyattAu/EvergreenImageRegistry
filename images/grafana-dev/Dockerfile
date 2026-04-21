# =============================================================================
# SOVEREIGN HARDENED GRAFANA-DEV
# Generated from template - Version: 10.4.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# Dev mode requires writable config and plugin directories
# =============================================================================

ARG VERSION=10.4.1
ARG BUILD_DATE

FROM debian:bookworm-20240101-slim AS downloader
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://dl.grafana.com/oss/release/grafana-${VERSION}.linux-amd64.tar.gz" -o /grafana.tar.gz && \
    echo "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2  /grafana.tar.gz" | sha256sum -c -
RUN tar -xzf /grafana.tar.gz -C /opt && \
    rm /grafana.tar.gz && \
    strip /opt/grafana-${VERSION}/bin/grafana-server && \
    strip /opt/grafana-${VERSION}/bin/grafana-cli

FROM debian:bookworm-20240101-slim
RUN groupadd -g 65534 grafana && \
    useradd -m -u 65534 -g grafana -s /usr/sbin/nologin grafana
COPY --from=downloader /opt/grafana-10.4.1/bin/grafana-server /usr/local/bin/grafana-server
COPY --from=downloader /opt/grafana-10.4.1/bin/grafana-cli /usr/local/bin/grafana-cli
COPY --from=downloader /opt/grafana-10.4.1/public /usr/share/grafana/public
COPY --from=downloader /opt/grafana-10.4.1/conf /etc/grafana
RUN mkdir -p /app/data /app/logs /app/plugins /app/conf/provisioning && \
    chown -R grafana:grafana /app /etc/grafana
USER 65534:65534
WORKDIR /app
EXPOSE 3000
ENV GF_PATHS_DATA=/app/data \
    GF_PATHS_LOGS=/app/logs \
    GF_PATHS_PLUGINS=/app/plugins \
    GF_PATHS_CONFIG=/app/conf/defaults.ini \
    GF_PATHS_PROVISIONING=/app/conf/provisioning \
    GF_DEFAULT_INSTANCE_NAME=grafana-dev \
    GF_ANALYTICS_REPORTING_ENABLED=false \
    GF_LOG_LEVEL=debug \
    GF_SERVER_ROUTER_LOGGING=true \
    GF_SECURITY_DISABLE_INITIAL_ADMIN_CREATION=true
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["/usr/local/bin/grafana-cli", "--version"]
ENTRYPOINT ["/usr/local/bin/grafana-server"]
LABEL org.opencontainers.image.title="grafana-dev" \
      org.opencontainers.image.version="10.4.1" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.description="Grafana OSS in development mode - debug logging, provisioning enabled" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="15000ms" \
      sovereign.hft.cpu-pins="2-3" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="recreate" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER" \
      sovereign.hft.runtime="go" \
      sovereign.hft.runtime-hints="GOMAXPROCS=<cores>"
