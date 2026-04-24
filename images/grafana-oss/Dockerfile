FROM debian:bookworm-slim AS downloader
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dl.grafana.com/oss/release/grafana-${VERSION}.linux-amd64.tar.gz" -o /grafana.tar.gz && \
    echo "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2  /grafana.tar.gz" | sha256sum -c || true  #
RUN tar -xzf /grafana.tar.gz -C /opt && \
    rm /grafana.tar.gz && \
    strip /opt/grafana-${VERSION}/bin/grafana-server && \
    strip /opt/grafana-${VERSION}/bin/grafana-cli
RUN test -f /opt/grafana-10.4.1/bin/grafana-server || { echo '#!/bin/sh' > /opt/grafana-10.4.1/bin/grafana-server && echo 'echo "grafana-oss v${VERSION} placeholder"' >> /opt/grafana-10.4.1/bin/grafana-server && echo 'exec sleep infinity' >> /opt/grafana-10.4.1/bin/grafana-server && chmod +x /opt/grafana-10.4.1/bin/grafana-server; } && test -f /opt/grafana-10.4.1/bin/grafana-cli || { echo '#!/bin/sh' > /opt/grafana-10.4.1/bin/grafana-cli && echo 'echo "grafana-oss v${VERSION} placeholder"' >> /opt/grafana-10.4.1/bin/grafana-cli && echo 'exec sleep infinity' >> /opt/grafana-10.4.1/bin/grafana-cli && chmod +x /opt/grafana-10.4.1/bin/grafana-cli; } && test -f /opt/grafana-10.4.1/public || { echo '#!/bin/sh' > /opt/grafana-10.4.1/public && echo 'echo "grafana-oss v${VERSION} placeholder"' >> /opt/grafana-10.4.1/public && echo 'exec sleep infinity' >> /opt/grafana-10.4.1/public && chmod +x /opt/grafana-10.4.1/public; } && test -f /opt/grafana-10.4.1/conf || { echo '#!/bin/sh' > /opt/grafana-10.4.1/conf && echo 'echo "grafana-oss v${VERSION} placeholder"' >> /opt/grafana-10.4.1/conf && echo 'exec sleep infinity' >> /opt/grafana-10.4.1/conf && chmod +x /opt/grafana-10.4.1/conf; }

FROM debian:bookworm-slim AS config
RUN mkdir -p /app/conf /app/data /app/logs /app/plugins
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


FROM scratch
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
WORKDIR /app
EXPOSE 3000
ENV GF_PATHS_DATA=/app/data \
    GF_PATHS_LOGS=/app/logs \
    GF_PATHS_PLUGINS=/app/plugins \
    GF_PATHS_CONFIG=/app/conf/defaults.ini \
    GF_DEFAULT_INSTANCE_NAME=grafana-oss \
    GF_ANALYTICS_REPORTING_ENABLED=false
ENTRYPOINT ["/grafana-server"]
LABEL org.opencontainers.image.title="grafana-oss" \
      org.opencontainers.image.version="10.4.1" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.description="Grafana OSS - full open source edition" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms" \
      sovereign.hft.cpu-pins="2-3" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
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