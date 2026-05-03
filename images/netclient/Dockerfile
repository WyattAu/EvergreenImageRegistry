ARG VERSION=v1.5.1

FROM gravitl/netclient:v1.5.1 AS upstream

FROM scratch
COPY --from=upstream /usr/bin/netclient /netclient
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 443

HEALTHCHECK NONE
ENTRYPOINT ["/netclient"]
LABEL org.opencontainers.image.title="netclient"       org.opencontainers.image.version="v1.5.1"       org.opencontainers.image.vendor="Gravitl"       org.opencontainers.image.source="https://github.com/gravitl/netmaker"       evergreen.image.tier="1"       evergreen.image.category="networking"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="3s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
