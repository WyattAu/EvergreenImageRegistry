ARG VERSION=2.7.3

FROM fallenbagel/jellyseerr:${VERSION} AS upstream

FROM scratch
COPY --from=upstream /app/jellyseerr /jellyseerr
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 5055
ENTRYPOINT ["/jellyseerr"]
LABEL org.opencontainers.image.title="jellyseer"       org.opencontainers.image.version="v3.2.0"       org.opencontainers.image.vendor="Jellyseerr"       org.opencontainers.image.source="https://github.com/Fallenbagel/jellyseerr"       sovereign.image.tier="2"       sovereign.image.category="media-streaming"       sovereign.image.status="functional"       sovereign.constraint.nonroot="true"       sovereign.constraint.base="scratch"       sovereign.hft.signal-handling="native"       sovereign.hft.shutdown-timeout="5s"       sovereign.hft.init-system="none"       sovereign.hft.startup-timeout="10000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
