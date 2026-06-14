ARG VERSION=2.4.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532



ARG SHIM_VERSION=v1.2.0

FROM viktorstrate/photoview:2.4.0@sha256:6b3777400d6a6ed3c30d0963326d176f688cd0204f5d835a40f43aef32982475 AS upstream



FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim


COPY --from=upstream /app/photoview /photoview

COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

WORKDIR /app

EXPOSE 80




HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/shim", "run"]

LABEL org.opencontainers.image.title="photoview"       org.opencontainers.image.version="v2.4.0"       org.opencontainers.image.vendor="photoview/photoview"       org.opencontainers.image.source="https://github.com/photoview/photoview"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.base="scratch"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="3s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="3000ms" \
org.opencontainers.image.description="photoview container image" \
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
