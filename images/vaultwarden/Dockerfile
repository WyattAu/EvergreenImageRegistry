ARG VERSION=1.35.8

FROM vaultwarden/server:1.35.8 AS upstream

FROM scratch
COPY --from=upstream /vaultwarden /vaultwarden
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/vaultwarden"]

LABEL org.opencontainers.image.title="vaultwarden"       org.opencontainers.image.version="1.35.8"       org.opencontainers.image.vendor="dani-garcia"       org.opencontainers.image.source="https://github.com/dani-garcia/vaultwarden"       sovereign.image.tier="2"       sovereign.image.category="secrets"       sovereign.image.status="functional"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"       sovereign.hft.signal-handling="native"       sovereign.hft.shutdown-timeout="3s"       sovereign.hft.init-system="none"       sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
