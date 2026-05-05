ARG VERSION=v1.5.1



FROM gravitl/netclient@sha256:2294714d5560b5fd1edba29f12fe29dd2b6f983b0400955f78b8562ba363d9ef AS upstream



FROM scratch

COPY --from=upstream /usr/bin/netclient /netclient

COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532

WORKDIR /app

EXPOSE 443



HEALTHCHECK NONE

ENTRYPOINT ["/netclient"]

LABEL org.opencontainers.image.title="netclient"       org.opencontainers.image.version="v1.5.1"       org.opencontainers.image.vendor="Gravitl"       org.opencontainers.image.source="https://github.com/gravitl/netmaker"       evergreen.image.tier="1"       evergreen.image.category="networking"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="3s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="3000ms" \
org.opencontainers.image.description="netclient container image" \
evergreen.base.image="scratch"

LABEL evergreen.metrics.native="ztunnel"

LABEL evergreen.health.type="exec"

LABEL evergreen.security.cap-drop="ALL"

LABEL evergreen.security.no-new-privileges="true"

LABEL evergreen.security.read-only-rootfs="true"

LABEL evergreen.security.seccomp="runtime-default"



EXPOSE 9101

STOPSIGNAL SIGTERM
