ARG VERSION=v2.4.0

FROM viktorstrate/photoview:v2.4.0 AS upstream

FROM scratch
COPY --from=upstream /app/photoview /photoview
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["/photoview"]
LABEL org.opencontainers.image.title="photoview"       org.opencontainers.image.version="v2.4.0"       org.opencontainers.image.vendor="photoview/photoview"       org.opencontainers.image.source="https://github.com/photoview/photoview"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.base="scratch"       sovereign.hft.signal-handling="native"       sovereign.hft.shutdown-timeout="3s"       sovereign.hft.init-system="none"       sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
