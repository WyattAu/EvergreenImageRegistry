ARG VERSION=3.2.51
ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM orientdb:${VERSION}
ARG VERSION

COPY --from=shim /shim /usr/local/bin/shim

ENV SHIM_METRICS_ENABLED="true"

HEALTHCHECK --interval=15s --timeout=5s --start-period=40s --retries=3 \

  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:2480"]

EXPOSE 2480 9101

LABEL org.opencontainers.image.title="orientdb" \
      org.opencontainers.image.description="OrientDB - multi-model NoSQL database (hardened with health-shim)" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Orientechnologies" \
      org.opencontainers.image.source="https://github.com/orientechnologies/orientdb" \
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
