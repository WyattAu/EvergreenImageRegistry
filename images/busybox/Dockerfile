ARG VERSION=1.37.0
ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache busybox ca-certificates 2>/dev/null || true && \
    mkdir -p /app /var/log/busybox 2>/dev/null || true

USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/bin/busybox"]
CMD ["sh"]

LABEL org.opencontainers.image.title="busybox" \
      org.opencontainers.image.description="BusyBox - Swiss army knife of embedded Linux utilities" \
      org.opencontainers.image.version="1.37.0" \
      org.opencontainers.image.vendor="busybox.net" \
      org.opencontainers.image.source="https://www.busybox.net/" \
      evergreen.image.tier="3" \
      evergreen.image.category="utilities" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="1000ms"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
