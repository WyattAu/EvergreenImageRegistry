ARG VERSION=3.1.2331
ARG SHIM_VERSION=v1.3.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM nxlog/nxlog:${VERSION}
ARG VERSION

COPY --from=shim /shim /usr/local/bin/shim

ENV SHIM_METRICS_ENABLED="true"

HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:514"]

EXPOSE 514 9101

LABEL org.opencontainers.image.title="nxlog" \
      org.opencontainers.image.description="NXLog Community Edition - log collection and forwarding (hardened with health-shim)" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="nxlog" \
      org.opencontainers.image.source="https://github.com/nxlogcommunity/nxlog" \
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
