ARG VERSION=25.04.9.4.1
ARG TARGETARCH

FROM collabora/code@sha256:a3b9e8a7f6c2d1e4b5c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b AS upstream

FROM scratch

COPY --from=upstream /opt/collaboraoffice /opt/collaboraoffice
COPY --from=upstream /usr/bin/loolwsd /usr/bin/loolwsd
COPY --from=upstream /etc/loolwsd /etc/loolwsd
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=upstream /usr/lib /usr/lib
COPY --from=upstream /lib /lib
COPY --from=upstream /var/log/collabora /var/log/collabora

USER 65532:65532

WORKDIR /app

EXPOSE 9980

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 CMD curl -sf http://localhost:9980/hosting/discovery || exit 1

ENTRYPOINT ["/usr/bin/loolwsd"]

LABEL org.opencontainers.image.title="collabora" \
      org.opencontainers.image.description="Collabora Online - LibreOffice-based online office suite" \
      org.opencontainers.image.version="25.04.9.4.1" \
      org.opencontainers.image.vendor="Collabora" \
      org.opencontainers.image.source="https://github.com/CollaboraOnline/online" \
      evergreen.image.tier="2" \
      evergreen.image.category="document-management" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="60000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

STOPSIGNAL SIGTERM
