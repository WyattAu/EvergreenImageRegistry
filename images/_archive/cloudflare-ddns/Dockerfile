ARG VERSION=1.16.2

FROM docker.io/favonia/cloudflare-ddns:${VERSION} AS source

FROM scratch
COPY --from=source /bin/ddns /cloudflare-ddns
COPY --from=source /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/cloudflare-ddns"]
LABEL org.opencontainers.image.title="cloudflare-ddns" \
      org.opencontainers.image.description="Cloudflare DDNS - dynamic DNS updater for Cloudflare" \
      org.opencontainers.image.version="1.16.2" \
      org.opencontainers.image.vendor="favonia" \
      org.opencontainers.image.source="https://github.com/favonia/cloudflare-ddns" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
