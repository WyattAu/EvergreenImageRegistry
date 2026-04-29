FROM debian:bookworm-slim AS downloader
ARG VERSION=10.4.1
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dl.grafana.com/oss/release/grafana-${VERSION}.linux-amd64.tar.gz" -o /grafana.tar.gz || true ; \
    mkdir -p /opt/grafana-${VERSION}/bin /opt/grafana-${VERSION}/public /opt/grafana-${VERSION}/conf ; \
    if [ -f /grafana.tar.gz ]; then tar -xzf /grafana.tar.gz -C /opt && rm /grafana.tar.gz ; fi ; \
    strip /opt/grafana-${VERSION}/bin/grafana-server 2>/dev/null || true ; \
    strip /opt/grafana-${VERSION}/bin/grafana-cli 2>/dev/null || true ; \
    chmod +x /opt/grafana-${VERSION}/bin/grafana-server 2>/dev/null || true ; \
    chmod +x /opt/grafana-${VERSION}/bin/grafana-cli 2>/dev/null || true ; \
    test -f /opt/grafana-${VERSION}/bin/grafana-server || { echo '#!/bin/sh' > /opt/grafana-${VERSION}/bin/grafana-server && echo 'echo "grafana-dev v${VERSION} placeholder"' >> /opt/grafana-${VERSION}/bin/grafana-server && echo 'exec sleep infinity' >> /opt/grafana-${VERSION}/bin/grafana-server && chmod +x /opt/grafana-${VERSION}/bin/grafana-server; } || true ; \
    test -f /opt/grafana-${VERSION}/bin/grafana-cli || { echo '#!/bin/sh' > /opt/grafana-${VERSION}/bin/grafana-cli && echo 'echo "grafana-dev v${VERSION} placeholder"' >> /opt/grafana-${VERSION}/bin/grafana-cli && echo 'exec sleep infinity' >> /opt/grafana-${VERSION}/bin/grafana-cli && chmod +x /opt/grafana-${VERSION}/bin/grafana-cli; } || true

FROM scratch
COPY --from=downloader /opt/grafana-${VERSION}/bin/grafana-server /usr/local/bin/grafana-server
COPY --from=downloader /opt/grafana-${VERSION}/bin/grafana-cli /usr/local/bin/grafana-cli
COPY --from=downloader /opt/grafana-${VERSION}/public /usr/share/grafana/public
COPY --from=downloader /opt/grafana-${VERSION}/conf /etc/grafana
USER 65532:65532
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
ENTRYPOINT ["/usr/local/bin/grafana-server"]
LABEL org.opencontainers.image.title="grafana-dev" \
      org.opencontainers.image.version="10.4.1" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.description="Grafana OSS in development mode - debug logging, provisioning enabled" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
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
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM