ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=v1.143.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.142.0/victoria-metrics-linux-${TARGETARCH}-v1.142.0-cluster.tar.gz -o /victoria-metrics.tar.gz ; \
    # TODO: update sha256 for new version
    echo "a9415aa4d6f666f1715ffd8b564128b3e3b468139b43b6ff1194ad3f5242ede3  /victoria-metrics.tar.gz" | sha256sum -c ; \
    [ -f /victoria-metrics.tar.gz ] && tar -xzf /victoria-metrics.tar.gz -C / && rm -f /victoria-metrics.tar.gz && chmod +x /victoria-metrics 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.142.0/victoria-metrics-linux-${TARGETARCH}-v1.142.0-cluster.tar.gz -o /victoria-metrics && chmod +x /victoria-metricsbinary not available - download failed" >&2"' >> /victoria-metrics && echo 'exit 1' >> /victoria-metrics && chmod +x /victoria-metrics; } && \
    mkdir -p /app /var/log/victoria-metrics /var/cache/victoria-metrics 2>/dev/null || true

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /victoria-metrics /victoria-metrics
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /app /app
COPY --from=downloader /var/log/victoria-metrics /var/log/victoria-metrics
COPY --from=downloader /var/cache/victoria-metrics /var/cache/victoria-metrics
USER 65532:65532
WORKDIR /app
EXPOSE 8428

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8428"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="victoriametrics" \
      org.opencontainers.image.description="VictoriaMetrics - fast, cost-effective time series database" \
      org.opencontainers.image.version="v1.143.0" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/VictoriaMetrics/VictoriaMetrics"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
