ARG VERSION=24.04.10.2
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG GITHUB_TOKEN
RUN apk add --no-cache ca-certificates curl gnupg && \
    mkdir -p /var/log/collabora /etc/loolwsd ; 2>/dev/null || true \
    chown -R 65532:65532 /var/log/collabora /etc/loolwsd
USER 65532:65532
WORKDIR /app
EXPOSE 9980

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9980/ || exit 1
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
