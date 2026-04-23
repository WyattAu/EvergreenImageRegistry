ARG VERSION=24.04.10.2
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates curl gnupg
RUN mkdir -p /var/log/collabora /etc/loolwsd \
    && chown -R 65532:65532 /var/log/collabora /etc/loolwsd
USER 65532:65532
WORKDIR /app
EXPOSE 9980
ENTRYPOINT ["/usr/bin/loolwsd"]
LABEL org.opencontainers.image.title="collabora-online-code" \
      org.opencontainers.image.version="24.04.10.2" \
      org.opencontainers.image.vendor="Collabora" \
      org.opencontainers.image.source="https://github.com/CollaboraOnline/online" \
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