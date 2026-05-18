ARG VERSION=4.4.17
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532



FROM pydio/cells:${VERSION} AS upstream



FROM scratch

COPY --from=upstream /cells /cells || true

COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt || true

USER 65532:65532

WORKDIR /app

EXPOSE 8081



HEALTHCHECK NONE

ENTRYPOINT ["/cells"]

LABEL org.opencontainers.image.title="pydio-agent"       org.opencontainers.image.version="v4.4.17"       org.opencontainers.image.vendor="Pydio"       org.opencontainers.image.source="https://github.com/pydio/cells"       evergreen.image.tier="2"       evergreen.image.category="cloud-storage"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.base="scratch"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="5s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="10000ms" \
org.opencontainers.image.description="pydio-agent container image" \
evergreen.base.image="scratch"

LABEL evergreen.metrics.native="ztunnel"

LABEL evergreen.health.type="exec"

LABEL evergreen.security.cap-drop="ALL"

LABEL evergreen.security.no-new-privileges="true"

LABEL evergreen.security.read-only-rootfs="true"

LABEL evergreen.security.seccomp="runtime-default"



EXPOSE 9101

STOPSIGNAL SIGTERM
