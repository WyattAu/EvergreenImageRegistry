ARG VERSION=24.04.10.2
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates curl gnupg && \
    mkdir -p /var/log/collabora /etc/loolwsd ; 2>/dev/null || true ; \
    chown -R 65532:65532 /var/log/collabora /etc/loolwsd
USER 65532:65532
WORKDIR /app
EXPOSE 9980

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9980/ || exit 1
ENTRYPOINT ["/usr/bin/loolwsd"]
LABEL org.opencontainers.image.title="collabora-online-code" \
      org.opencontainers.image.description="collabora-online-code container image" \
      org.opencontainers.image.version="24.04.10.2" \
      org.opencontainers.image.vendor="Collabora" \
      org.opencontainers.image.source="https://github.com/CollaboraOnline/online" \
      evergreen.image.tier="2" \
      evergreen.image.category="document-management" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="60000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
