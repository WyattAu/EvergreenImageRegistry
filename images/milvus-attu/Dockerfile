ARG VERSION=2.4.9
ARG TARGETARCH

FROM docker.io/zilliz/attu:v2.4.9 AS upstream

FROM scratch
COPY --from=upstream /opt/attu/attu /attu
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 3000

HEALTHCHECK NONE
ENTRYPOINT ["/attu"]
LABEL org.opencontainers.image.title="milvus-attu" \
      org.opencontainers.image.description="milvus-attu container image" \
      org.opencontainers.image.version="2.4.9" \
      org.opencontainers.image.vendor="zilliztech/attu" \
      org.opencontainers.image.source="https://github.com/zilliztech/attu/releases/download/v2.4.9" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
