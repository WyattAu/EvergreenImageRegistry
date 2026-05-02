ARG VERSION=latest

FROM ghcr.io/gethomepage/homepage:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/homepage-sync /var/cache/homepage-sync 2>/dev/null || true


FROM scratch
COPY --from=upstream /app/homepage /usr/local/bin/homepage
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/homepage-sync /var/log/homepage-sync
COPY --from=builder /var/cache/homepage-sync /var/cache/homepage-sync

WORKDIR /app

EXPOSE 3000
EXPOSE 9101

LABEL org.opencontainers.image.title="homepage-sync" org.opencontainers.image.description="Homepage - sync mode" org.opencontainers.image.vendor="benphelps" org.opencontainers.image.source="https://github.com/benphelps/homepage" sovereign.image.tier="3" sovereign.constraint.nonroot="true" sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["homepage"]

CMD ["--config", "/app/config", "--enable-sync"]
