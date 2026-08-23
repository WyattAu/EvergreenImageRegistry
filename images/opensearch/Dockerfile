ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM opensearchproject/opensearch:2.12.0@sha256:645d3d9390ade7ebef988d3c9bc61a6616f1863ff41efe97e2347d6bf7972504
COPY --from=shim /shim /usr/local/bin/shim

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
RUN mkdir -p /usr/share/opensearch/data && chown -R 65532:65532 /usr/share/opensearch/data
USER 65532:65532
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9200"]


ENV SHIM_METRICS_ENABLED="true"

LABEL evergreen.entrypoint.pattern="repack-upstream-init"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9200 9101
LABEL prometheus.io/scrape="true" prometheus.io/port="9101" prometheus.io/path="/metrics"
LABEL evergreen.image.tier="critical"
STOPSIGNAL SIGTERM
