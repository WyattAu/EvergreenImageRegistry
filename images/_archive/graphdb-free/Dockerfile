ARG VERSION=latest
ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM ontotext/graphdb-free:${VERSION}
ARG VERSION

COPY --from=shim /shim /usr/local/bin/shim

ENV SHIM_METRICS_ENABLED="true"

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:7200"]

EXPOSE 7200 9101

LABEL org.opencontainers.image.title="graphdb-free" \
      org.opencontainers.image.description="GraphDB Free - semantic graph database (hardened with health-shim)" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Ontotext" \
      evergreen.image.tier="standard"
LABEL evergreen.entrypoint.pattern="repack-upstream-init"
LABEL evergreen.base.image="upstream"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
