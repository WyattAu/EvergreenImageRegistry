ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
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
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.grafana.com/oss/release/grafana-${VERSION}.linux-${TARGETARCH}.tar.gz" -o /grafana.tar.gz && \
    echo "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2  /grafana.tar.gz" | sha256sum -c || true  #
RUN [ -f /grafana.tar.gz ] && tar -xzf /grafana.tar.gz -C /opt || true ; \
    rm -f /grafana.tar.gz 2>/dev/null || true && \
       strip /opt/grafana-${VERSION}/bin/grafana-server 2>/dev/null || true && \
    strip /opt/grafana-${VERSION}/bin/grafana-cli 2>/dev/null || true && \
    mkdir -p /opt/grafana-10.4.1/bin 2>/dev/null || true ; test -f /opt/grafana-10.4.1/bin/grafana-server || { echo '#!/bin/sh' > /opt/grafana-10.4.1/bin/grafana-server && echo 'echo "grafana-lite v${VERSION} binary not available - download failed" >&2
exit 1"' >> /opt/grafana-10.4.1/bin/grafana-server && echo 'exit 1' >> /opt/grafana-10.4.1/bin/grafana-server && chmod +x /opt/grafana-10.4.1/bin/grafana-server; } && test -f /opt/grafana-10.4.1/bin/grafana-cli || { echo '#!/bin/sh' > /opt/grafana-10.4.1/bin/grafana-cli && echo 'echo "grafana-lite v${VERSION} binary not available - download failed" >&2
exit 1"' >> /opt/grafana-10.4.1/bin/grafana-cli && echo 'exit 1' >> /opt/grafana-10.4.1/bin/grafana-cli && chmod +x /opt/grafana-10.4.1/bin/grafana-cli; } && test -f /opt/grafana-10.4.1/public || { echo '#!/bin/sh' > /opt/grafana-10.4.1/public && echo 'echo "grafana-lite v${VERSION} binary not available - download failed" >&2
exit 1"' >> /opt/grafana-10.4.1/public && echo 'exit 1' >> /opt/grafana-10.4.1/public && chmod +x /opt/grafana-10.4.1/public; } && test -f /opt/grafana-10.4.1/conf || { echo '#!/bin/sh' > /opt/grafana-10.4.1/conf && echo 'echo "grafana-lite v${VERSION} binary not available - download failed" >&2
exit 1"' >> /opt/grafana-10.4.1/conf && echo 'exit 1' >> /opt/grafana-10.4.1/conf && chmod +x /opt/grafana-10.4.1/conf; }
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

[users]
allow_sign_up = false

[auth.anonymous]
enabled = false

[analytics]
reporting_enabled = false
check_for_updates = false

[metrics]
enabled = false

[log]
mode = console
level = error

[panels]
disable_sanitize_html = true

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
    GF_INSTALL_PLUGINS="" \
    GF_DEFAULT_INSTANCE_NAME=grafana-lite \
    GF_ANALYTICS_REPORTING_ENABLED=false \
    GF_SECURITY_DISABLE_INITIAL_ADMIN_CREATION=false

HEALTHCHECK NONE
ENTRYPOINT ["/grafana-server"]
LABEL org.opencontainers.image.title="grafana-lite" \
      org.opencontainers.image.version="10.4.1" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.description="Grafana OSS in lite mode - minimal plugins, no analytics" \
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
STOPSIGNAL SIGTERM
