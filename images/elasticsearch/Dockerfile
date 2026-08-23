ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM docker.elastic.co/elasticsearch/elasticsearch:8.14.0@sha256:62c1f372cb76be4929a50edbbba96204c5b4ff91f1d12b7839a95b1a1274e7eb
COPY --from=shim /shim /usr/local/bin/shim

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
RUN mkdir -p /usr/share/elasticsearch/data && chown -R 65532:65532 /usr/share/elasticsearch/data
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
