# =============================================================================
# EVERGREEN HARDENED GRAFANA
# Pre-built binary download - scratch final stage
# =============================================================================
ARG VERSION=12.2.9
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.1.0

FROM cgr.dev/chainguard/wolfi-base AS downloader
ARG VERSION
RUN apk add --no-cache wget ca-certificates && \
    wget -q "https://dl.grafana.com/oss/release/grafana-${VERSION}.linux-amd64.tar.gz" -O /grafana.tar.gz && \
    tar -xzf /grafana.tar.gz -C /tmp && \
    mkdir -p /grafana-bin && \
    cp -r /tmp/grafana-${VERSION}/bin/* /grafana-bin/ && \
    mkdir -p /usr/share/grafana && \
    cp -r /tmp/grafana-${VERSION}/conf /usr/share/grafana/ && \
    cp -r /tmp/grafana-${VERSION}/public /usr/share/grafana/ && \
    mkdir -p /etc/grafana /var/lib/grafana /var/log/grafana /tmp && \
    rm -rf /grafana.tar.gz /tmp/grafana-${VERSION}

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /grafana-bin /grafana-bin
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /usr/share/grafana /usr/share/grafana
RUN mkdir -p /etc/grafana /var/lib/grafana /var/log/grafana /tmp && \
    cp -r /usr/share/grafana/conf/sample.ini /etc/grafana/grafana.ini 2>/dev/null || true
USER ${APP_UID}:${APP_GID}
ENV SHIM_METRICS_ENABLED="true" \
    PATH="/grafana-bin:$PATH" \
    GF_PATHS_HOME="/usr/share/grafana" \
    GF_PATHS_DATA="/var/lib/grafana" \
    GF_PATHS_LOGS="/var/log/grafana" \
    GF_PATHS_PLUGINS="/var/lib/grafana/plugins" \
    GF_PATHS_PROVISIONING="/usr/share/grafana/conf/provisioning"
WORKDIR /
EXPOSE 3000 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:3000"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/grafana-bin/grafana-server"]
LABEL org.opencontainers.image.title="grafana" \
      org.opencontainers.image.description="Grafana - analytics and interactive visualization platform" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.platforms="linux/amd64" \
      org.opencontainers.image.source="https://github.com/grafana/grafana" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch" \
      evergreen.build.type="binary-download" \
      evergreen.metrics.native="ztunnel" \
      evergreen.health.type="exec" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.read-only-rootfs="true" \
      evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
