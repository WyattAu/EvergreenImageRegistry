ARG VERSION=2.4.4-bookworm-slim
ARG SHIM_VERSION=v1.3.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM rethinkdb:${VERSION}
ARG VERSION

COPY --from=shim /shim /usr/local/bin/shim

ENV SHIM_METRICS_ENABLED="true"

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:28015"]

EXPOSE 28015 9101

LABEL org.opencontainers.image.title="rethinkdb" \
      org.opencontainers.image.description="RethinkDB - real-time NoSQL database (hardened with health-shim)" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="RethinkDB" \
      org.opencontainers.image.source="https://github.com/rethinkdb/rethinkdb" \
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
