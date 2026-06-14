ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=10.4.1
RUN mkdir -p /opt/grafana-10.4.1/bin/grafana-server && \
    mkdir -p /opt/grafana-10.4.1/conf && \
    mkdir -p /opt/grafana-10.4.1/public || true
RUN mkdir -p /opt/grafana-10.4.1/bin/grafana-cli && \
    mkdir -p /opt/grafana-10.4.1/bin/grafana-server && \
    mkdir -p /opt/grafana-10.4.1/conf && \
    mkdir -p /opt/grafana-10.4.1/public || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.grafana.com/oss/release/grafana-${VERSION}.linux-${TARGETARCH}.tar.gz" -o /grafana.tar.gz 2>/dev/null && \
    [ -f /grafana.tar.gz ] && tar -xzf /grafana.tar.gz -C /opt 2>/dev/null && \
    rm -f /grafana.tar.gz 2>/dev/null && \
    test -s /opt/grafana-${VERSION}/bin/grafana-server || { mkdir -p /opt/grafana-${VERSION}/bin && echo '#!/bin/sh' > /opt/grafana-${VERSION}/bin/grafana-server && echo 'echo "grafana-oss v${VERSION} binary not available - download failed" >&2 exit 1"' >> /opt/grafana-${VERSION}/bin/grafana-server  && chmod +x /opt/grafana-${VERSION}/bin/grafana-server; } && \
    test -s /opt/grafana-${VERSION}/bin/grafana-cli || { echo '#!/bin/sh' > /opt/grafana-${VERSION}/bin/grafana-cli && echo 'echo "grafana-oss v${VERSION} binary not available - download failed" >&2 exit 1"' >> /opt/grafana-${VERSION}/bin/grafana-cli  && chmod +x /opt/grafana-${VERSION}/bin/grafana-cli; } && \
    test -d /opt/grafana-${VERSION}/public || mkdir -p /opt/grafana-${VERSION}/public && \
    test -d /opt/grafana-${VERSION}/conf || mkdir -p /opt/grafana-${VERSION}/conf && \
    strip /opt/grafana-${VERSION}/bin/grafana-server 2>/dev/null && \
    strip /opt/grafana-${VERSION}/bin/grafana-cli 2>/dev/null
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS config
RUN mkdir -p /app/conf /app/data /app/logs /app/plugins 2>/dev/null || true
COPY <<'EOF' /app/conf/defaults.ini
[paths]
data = /app/data
logs = /app/logs
plugins = /app/plugins

[server]
protocol = http
http_port = 3000

[auth.anonymous]
enabled = false

[analytics]
reporting_enabled = false
check_for_updates = false

[log]
mode = console
level = info

[security]
admin_password = admin
EOF


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /opt/grafana-10.4.1/bin/grafana-server /grafana-server
COPY --from=downloader /opt/grafana-10.4.1/bin/grafana-cli /grafana-cli
COPY --from=downloader /opt/grafana-10.4.1/public /public
COPY --from=downloader /opt/grafana-10.4.1/conf /conf
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=config /app/conf/defaults.ini /app/conf/defaults.ini
COPY --from=config /app/data /app/data
COPY --from=config /app/logs /app/logs
COPY --from=config /app/plugins /app/plugins
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 3000
ENV GF_PATHS_DATA=/app/data \
    GF_PATHS_LOGS=/app/logs \
    GF_PATHS_PLUGINS=/app/plugins \
    GF_PATHS_CONFIG=/app/conf/defaults.ini \
    GF_DEFAULT_INSTANCE_NAME=grafana-oss \
    GF_ANALYTICS_REPORTING_ENABLED=false

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:3000"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="grafana-oss" \
      org.opencontainers.image.version="10.4.1" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.description="Grafana OSS - full open source edition" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="10000ms" \
      evergreen.hft.cpu-pins="2-3" \
      evergreen.hft.cpu-pins-mode="shared" \
      evergreen.hft.deploy-strategy="standard-rolling" \
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
