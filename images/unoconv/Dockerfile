ARG VERSION=0.8
ARG TARGETARCH
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG GITHUB_TOKEN
RUN apk add --no-cache ca-certificates curl && \
    mkdir -p /app /var/log/app /var/cache/app ; 2>/dev/null || true ; \
    chown -R 65532:65532 /app /var/log/app /var/cache/app
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["unoconv"]
LABEL org.opencontainers.image.title="unoconv" \
      org.opencontainers.image.description="unoconv container image" \
      org.opencontainers.image.version="0.8" \
      org.opencontainers.image.vendor="Unoconv" \
      org.opencontainers.image.source="https://github.com/dagwieers/unoconv" \
      evergreen.image.tier="2" \
      evergreen.image.category="document-management" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
