ARG VERSION=30.2

FROM typesense/typesense:30.2 AS upstream

FROM scratch
COPY --from=upstream /usr/bin/typesense-server /typesense-server
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8108

HEALTHCHECK NONE
ENTRYPOINT ["/typesense-server"]
LABEL org.opencontainers.image.title="typesense"       org.opencontainers.image.version="30.2"       org.opencontainers.image.vendor="Typesense"       org.opencontainers.image.source="https://github.com/typesense/typesense"       org.opencontainers.image.description="Fast, typo-tolerant search engine"       evergreen.image.tier="1"       evergreen.image.category="search"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.base="scratch"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="5s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="5000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
