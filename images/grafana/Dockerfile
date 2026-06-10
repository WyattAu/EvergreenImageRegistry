# =============================================================================
# EVERGREEN HARDENED GRAFANA
# Pre-built binary download - scratch final stage
# =============================================================================
ARG VERSION=12.2.9
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.0.0

FROM debian:bookworm-slim AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends wget ca-certificates && rm -rf /var/lib/apt/lists/* && \
    wget -q "https://dl.grafana.com/oss/release/grafana-${VERSION}.linux-amd64.tar.gz" -O /grafana.tar.gz && \
    tar -xzf /grafana.tar.gz -C /tmp && \
    cp /tmp/grafana-${VERSION}/bin/grafana-server /grafana-server && \
    chmod +x /grafana-server && \
    mkdir -p /etc/grafana /var/lib/grafana /var/log/grafana && \
    cp -r /tmp/grafana-${VERSION}/conf/* /etc/grafana/ && \
    rm -rf /grafana.tar.gz /tmp/grafana-${VERSION}

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim
COPY --from=downloader /grafana-server /grafana-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /etc/grafana /etc/grafana
USER ${APP_UID}:${APP_GID}
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /
EXPOSE 3000 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:3000"]

ENTRYPOINT ["/shim", "run", "-c", "/grafana-server"]
CMD ["--homepath=/usr/share/grafana", "--config=/etc/grafana/grafana.ini"]
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
