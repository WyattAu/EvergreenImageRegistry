ARG VERSION=2.7.3
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532



ARG SHIM_VERSION=v1.0.0

FROM fallenbagel/jellyseerr:${VERSION} AS upstream



FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim


COPY --from=upstream /app/jellyseerr /jellyseerr

COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

WORKDIR /app

EXPOSE 5055




HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:5055"]

ENTRYPOINT ["/shim", "run"]

LABEL org.opencontainers.image.title="jellyseer"       org.opencontainers.image.version="2.7.3"       org.opencontainers.image.vendor="Jellyseerr"       org.opencontainers.image.source="https://github.com/Fallenbagel/jellyseerr"       evergreen.image.tier="2"       evergreen.image.category="media-streaming"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.base="scratch"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="5s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="10000ms" \
org.opencontainers.image.description="jellyseer container image" \
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
