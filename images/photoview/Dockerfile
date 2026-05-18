ARG VERSION=2.4.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532



FROM viktorstrate/photoview:2.4.0 AS upstream



FROM scratch

COPY --from=upstream /app/photoview /photoview

COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532

WORKDIR /app

EXPOSE 80



HEALTHCHECK NONE

ENTRYPOINT ["/photoview"]

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

STOPSIGNAL SIGTERM
