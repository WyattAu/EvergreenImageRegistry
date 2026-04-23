ARG VERSION=8.2.2
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates curl gnupg s "
RUN mkdir -p /var/log/onlyoffice /var/lib/onlyoffice \
    && chown -R 65532:65532 /var/log/onlyoffice /var/lib/onlyoffice
USER 65532:65532
WORKDIR /app
EXPOSE 80 443
ENTRYPOINT ["/usr/bin/ds"]
LABEL org.opencontainers.image.title="onlyoffice-controlpanel" \
      org.opencontainers.image.version="8.2.2" \
      org.opencontainers.image.vendor="ONLYOFFICE" \
      org.opencontainers.image.source="https://github.com/ONLYOFFICE/DocumentServer" \
      sovereign.image.tier="2" \
      sovereign.image.category="document-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM