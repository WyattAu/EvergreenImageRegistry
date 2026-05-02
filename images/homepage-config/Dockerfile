ARG VERSION=latest

FROM ghcr.io/gethomepage/homepage:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/homepage-config /var/cache/homepage-config 2>/dev/null || true


FROM scratch
COPY --from=upstream /app/homepage /usr/local/bin/homepage
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/homepage-config /var/log/homepage-config
COPY --from=builder /var/cache/homepage-config /var/cache/homepage-config

WORKDIR /app

EXPOSE 3000
EXPOSE 9101

LABEL org.opencontainers.image.title="homepage-config" org.opencontainers.image.description="Homepage - config mode" org.opencontainers.image.vendor="benphelps" org.opencontainers.image.source="https://github.com/benphelps/homepage" sovereign.image.tier="3" sovereign.constraint.nonroot="true" sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["homepage"]

CMD ["--config", "/app/config"]
