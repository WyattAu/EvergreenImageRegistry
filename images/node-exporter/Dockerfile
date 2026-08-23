ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM prom/node-exporter:v1.9.1@sha256:d00a542e409ee618a4edc67da14dd48c5da66726bbd5537ab2af9c1dfc442c8a
COPY --from=shim /shim /usr/local/bin/shim

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9100"]


ENV SHIM_METRICS_ENABLED="true"

LABEL evergreen.entrypoint.pattern="repack-upstream-init"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9100 9101
LABEL prometheus.io/scrape="true" prometheus.io/port="9101" prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM



LABEL org.opencontainers.image.title="node-exporter" \
      evergreen.image.tier="2"




USER 65532:65532
