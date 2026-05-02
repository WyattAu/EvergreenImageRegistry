ARG VERSION=v1.5.1

FROM gravitl/netclient:v1.5.1 AS upstream

FROM scratch
COPY --from=upstream /usr/bin/netclient /netclient
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 443
ENTRYPOINT ["/netclient"]
LABEL org.opencontainers.image.title="netclient"       org.opencontainers.image.version="v1.5.1"       org.opencontainers.image.vendor="Gravitl"       org.opencontainers.image.source="https://github.com/gravitl/netmaker"       sovereign.image.tier="1"       sovereign.image.category="networking"       sovereign.image.status="functional"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"       sovereign.hft.signal-handling="native"       sovereign.hft.shutdown-timeout="3s"       sovereign.hft.init-system="none"       sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
