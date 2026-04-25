ARG VERSION=24.8.2
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates curl || true
RUN mkdir -p /app /var/log/app /var/cache/app \ 2>/dev/null || true ; \
    chown -R 65532:65532 /app /var/log/app /var/cache/appUSER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["libreoffice"]
LABEL org.opencontainers.image.title="libreoffice-headless" \
      org.opencontainers.image.version="24.8.2" \
      org.opencontainers.image.vendor="LibreOffice" \
      org.opencontainers.image.source="https://www.libreoffice.org/" \
      sovereign.image.tier="2" \
      sovereign.image.category="document-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM