ARG VERSION=4.4.17

FROM pydio/cells:${VERSION} AS upstream

FROM scratch
COPY --from=upstream /cells /cells
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8081
ENTRYPOINT ["/cells"]
LABEL org.opencontainers.image.title="pydio-agent"       org.opencontainers.image.version="v4.4.17"       org.opencontainers.image.vendor="Pydio"       org.opencontainers.image.source="https://github.com/pydio/cells"       sovereign.image.tier="2"       sovereign.image.category="cloud-storage"       sovereign.image.status="functional"       sovereign.constraint.nonroot="true"       sovereign.constraint.base="scratch"       sovereign.hft.signal-handling="native"       sovereign.hft.shutdown-timeout="5s"       sovereign.hft.init-system="none"       sovereign.hft.startup-timeout="10000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
