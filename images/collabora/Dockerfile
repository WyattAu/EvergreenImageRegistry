ARG VERSION=25.04.9.4.1
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM collabora/code:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN mkdir -p /opt/collaboraoffice /usr/local/bin /etc/loolwsd /tmp/collabora-libs 2>/dev/null || true && \
    cp -a /upstream/usr/bin/loolwsd /usr/local/bin/loolwsd 2>/dev/null || true && \
    cp -a /upstream/etc/loolwsd/* /etc/loolwsd/ 2>/dev/null || true && \
    cp -a /upstream/usr/lib/* /tmp/collabora-libs/ 2>/dev/null || true && \
    cp -a /upstream/lib/* /tmp/collabora-libs/ 2>/dev/null || true && \
    mkdir -p /opt/collaboraoffice 2>/dev/null || true
COPY --from=upstream /opt/collaboraoffice/ /opt/collaboraoffice/

USER 65532:65532
WORKDIR /app

EXPOSE 9980

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 CMD wget -qO- http://localhost:9980/hosting/discovery || exit 1

ENTRYPOINT ["/usr/bin/loolwsd"]
LABEL org.opencontainers.image.title="collabora" \
      org.opencontainers.image.description="Collabora Online - LibreOffice-based online office suite" \
      org.opencontainers.image.version="25.04.9.4.1" \
      org.opencontainers.image.vendor="Collabora" \
      org.opencontainers.image.source="https://github.com/CollaboraOnline/online" \
      evergreen.image.tier="critical" \
      evergreen.image.category="document-management" \
      evergreen.constraint.nonroot="true" \
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
