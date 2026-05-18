ARG VERSION=1.35.8
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532



FROM vaultwarden/server@sha256:c4f6056fe0c288a052a223cecd263a90d1dda1a0177bb5b054a363a6c7b211d9 AS upstream



FROM scratch

COPY --from=upstream /vaultwarden /vaultwarden

COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532

WORKDIR /app

EXPOSE 8080



HEALTHCHECK NONE

ENTRYPOINT ["/vaultwarden"]



LABEL org.opencontainers.image.title="vaultwarden-alpine"       org.opencontainers.image.version="1.35.8"       org.opencontainers.image.vendor="dani-garcia"       org.opencontainers.image.source="https://github.com/dani-garcia/vaultwarden"       evergreen.image.tier="2"       evergreen.image.category="secrets"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="3s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="3000ms" \
org.opencontainers.image.description="vaultwarden-alpine container image" \
evergreen.base.image="scratch"

LABEL evergreen.metrics.native="ztunnel"

LABEL evergreen.health.type="exec"

LABEL evergreen.security.cap-drop="ALL"

LABEL evergreen.security.no-new-privileges="true"

LABEL evergreen.security.read-only-rootfs="true"

LABEL evergreen.security.seccomp="runtime-default"



EXPOSE 9101

STOPSIGNAL SIGTERM
