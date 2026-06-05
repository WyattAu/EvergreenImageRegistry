ARG VERSION=4.4.17
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532



ARG SHIM_VERSION=v0.3.0

FROM pydio/cells:${VERSION} AS upstream



FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim


COPY --from=upstream /cells /cells

COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

WORKDIR /app

EXPOSE 8081




HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8081"]

ENTRYPOINT ["/shim", "run"]

LABEL org.opencontainers.image.title="pydio-agent"       org.opencontainers.image.version="v4.4.17"       org.opencontainers.image.vendor="Pydio"       org.opencontainers.image.source="https://github.com/pydio/cells"       evergreen.image.tier="2"       evergreen.image.category="cloud-storage"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.base="scratch"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="5s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="10000ms" \
org.opencontainers.image.description="pydio-agent container image" \
evergreen.base.image="scratch"

LABEL evergreen.metrics.native="ztunnel"

LABEL evergreen.health.type="exec"

LABEL evergreen.security.cap-drop="ALL"

LABEL evergreen.security.no-new-privileges="true"

LABEL evergreen.security.read-only-rootfs="true"

LABEL evergreen.security.seccomp="runtime-default"



EXPOSE 9101

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
