ARG VERSION=latest

FROM ghcr.io/ltiam/apachedirectorystudio:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
COPY --from=upstream /opt/ApacheDirectoryStudio /opt/ApacheDirectoryStudio
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/ApacheDirectoryStudio 2>/dev/null || true

WORKDIR /app

EXPOSE 9101

LABEL org.opencontainers.image.title="ldapbrowser" org.opencontainers.image.version="2.0.0" org.opencontainers.image.vendor="Apache" org.opencontainers.image.source="https://github.com/ltiam/APacheDirectoryStudio" sovereign.image.tier="2" sovereign.image.category="identity" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.constraint.base="wolfi" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="5s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="15000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/opt/ApacheDirectoryStudio/ApacheDirectoryStudio"]
