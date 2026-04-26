ARG VERSION=0.8
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
ARG GITHUB_TOKEN
RUN apk add --no-cache ca-certificates curl 
RUN mkdir -p /app /var/log/app /var/cache/app ; \
    chown -R 65532:65532 /app /var/log/app /var/cache/appUSER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["unoconv"]
LABEL org.opencontainers.image.title="unoconv" \
      org.opencontainers.image.version="0.8" \
      org.opencontainers.image.vendor="Unoconv" \
      org.opencontainers.image.source="https://github.com/dagwieers/unoconv" \
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