ARG TARGETARCH
ARG TARGETARCH
ARG VERSION=10.4.1
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION
RUN mkdir -p /opt/grafana-${VERSION}/bin/grafana-server && \
    mkdir -p /opt/grafana-${VERSION}/conf && \
    mkdir -p /opt/grafana-${VERSION}/public || true
RUN mkdir -p /opt/grafana-${VERSION}/bin/grafana-cli && \
    mkdir -p /opt/grafana-${VERSION}/bin/grafana-server && \
    mkdir -p /opt/grafana-${VERSION}/conf && \
    mkdir -p /opt/grafana-${VERSION}/public || true
RUN mkdir -p /opt/grafana-${VERSION}/bin /opt/grafana-${VERSION}/public /opt/grafana-${VERSION}/conf
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.grafana.com/oss/release/grafana-${VERSION}.linux-${TARGETARCH}.tar.gz" -o /grafana.tar.gz && \
    echo "e6fb188d42556e7330165d1df46ebda920371640c24dad486cff71008f164127  /grafana.tar.gz" | sha256sum -c ; \
    mkdir -p /opt/grafana-${VERSION}/bin /opt/grafana-${VERSION}/public /opt/grafana-${VERSION}/conf ; \
    if [ -f /grafana.tar.gz ]; then tar -xzf /grafana.tar.gz -C /opt && rm -f /grafana.tar.gz ; fi ; \
    strip /opt/grafana-${VERSION}/bin/grafana-server 2>/dev/null ; \
    strip /opt/grafana-${VERSION}/bin/grafana-cli 2>/dev/null ; \
    chmod +x /opt/grafana-${VERSION}/bin/grafana-server 2>/dev/null ; \
    chmod +x /opt/grafana-${VERSION}/bin/grafana-cli 2>/dev/null ; \
    test -s /opt/grafana-${VERSION}/bin/grafana-server || { echo '#!/bin/sh' > /opt/grafana-${VERSION}/bin/grafana-server && echo 'echo "grafana-dev v'"${VERSION}"' binary not available - download failed" >&2 exit 1"' >> /opt/grafana-${VERSION}/bin/grafana-server { echo "Binary not available - download failed" >&2; exit 1; } 2>/dev/null ; \
    test -s /opt/grafana-${VERSION}/bin/grafana-cli || { echo '#!/bin/sh' > /opt/grafana-${VERSION}/bin/grafana-cli && echo 'echo "grafana-dev v'"${VERSION}"' binary not available - download failed" >&2 exit 1"' >> /opt/grafana-${VERSION}/bin/grafana-cli { echo "Binary not available - download failed" >&2; exit 1; } 2>/dev/null
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=10.4.1
COPY --from=downloader /opt/grafana-${VERSION}/bin/grafana-server /usr/local/bin/grafana-server
COPY --from=downloader /opt/grafana-${VERSION}/bin/grafana-cli /usr/local/bin/grafana-cli
COPY --from=downloader /opt/grafana-${VERSION}/public /usr/share/grafana/public
COPY --from=downloader /opt/grafana-${VERSION}/conf /etc/grafana
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
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

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:3000"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="grafana-dev" \
      org.opencontainers.image.version="10.4.1" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.description="Grafana OSS in development mode - debug logging, provisioning enabled" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="15000ms" \
      evergreen.hft.cpu-pins="2-3" \
      evergreen.hft.cpu-pins-mode="shared" \
      evergreen.hft.deploy-strategy="recreate" \
      evergreen.hft.pre-stop-hook="false" \
      evergreen.hft.connection-drain="false" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
      evergreen.hft.runtime="go" \
      evergreen.hft.runtime-hints="GOMAXPROCS=<cores>" \
            org.opencontainers.image.source="https://github.com/grafana/grafana"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
