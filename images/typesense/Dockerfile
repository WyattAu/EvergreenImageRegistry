ARG VERSION=30.2

FROM typesense/typesense:30.2 AS upstream

FROM scratch
COPY --from=upstream /usr/bin/typesense-server /typesense-server
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8108
ENTRYPOINT ["/typesense-server"]
LABEL org.opencontainers.image.title="typesense"       org.opencontainers.image.version="30.2"       org.opencontainers.image.vendor="Typesense"       org.opencontainers.image.source="https://github.com/typesense/typesense"       org.opencontainers.image.description="Fast, typo-tolerant search engine"       sovereign.image.tier="1"       sovereign.image.category="search"       sovereign.image.status="functional"       sovereign.constraint.nonroot="true"       sovereign.constraint.base="scratch"       sovereign.hft.signal-handling="native"       sovereign.hft.shutdown-timeout="5s"       sovereign.hft.init-system="none"       sovereign.hft.startup-timeout="5000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
