ARG VERSION=2.7.3
ARG TARGETARCH



FROM fallenbagel/jellyseerr:${VERSION} AS upstream



FROM scratch

COPY --from=upstream /app/jellyseerr /jellyseerr

COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532

WORKDIR /app

EXPOSE 5055



HEALTHCHECK NONE

ENTRYPOINT ["/jellyseerr"]

LABEL org.opencontainers.image.title="jellyseer"       org.opencontainers.image.version="v3.2.0"       org.opencontainers.image.vendor="Jellyseerr"       org.opencontainers.image.source="https://github.com/Fallenbagel/jellyseerr"       evergreen.image.tier="2"       evergreen.image.category="media-streaming"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.base="scratch"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="5s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="10000ms" \
org.opencontainers.image.description="jellyseer container image" \
evergreen.base.image="scratch"

LABEL evergreen.metrics.native="ztunnel"

LABEL evergreen.health.type="exec"

LABEL evergreen.security.cap-drop="ALL"

LABEL evergreen.security.no-new-privileges="true"

LABEL evergreen.security.read-only-rootfs="true"

LABEL evergreen.security.seccomp="runtime-default"



EXPOSE 9101

STOPSIGNAL SIGTERM
