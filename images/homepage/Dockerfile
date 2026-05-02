ARG VERSION=latest

FROM ghcr.io/gethomepage/homepage:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/homepage /var/cache/homepage 2>/dev/null || true


FROM scratch
COPY --from=upstream /app/homepage /homepage
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/homepage /var/log/homepage
COPY --from=builder /var/cache/homepage /var/cache/homepage

WORKDIR /app

EXPOSE 3000
EXPOSE 9101

LABEL org.opencontainers.image.title="homepage" org.opencontainers.image.description="Homepage - Application dashboard" org.opencontainers.image.vendor="benphelps" org.opencontainers.image.source="https://github.com/benphelps/homepage" sovereign.image.tier="3" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/homepage"]
