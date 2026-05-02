ARG VERSION=latest

FROM ghcr.io/pawelmalak/flame:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/flame /var/cache/flame 2>/dev/null || true


FROM scratch
COPY --from=upstream /app/flame /flame
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/flame /var/log/flame
COPY --from=builder /var/cache/flame /var/cache/flame

WORKDIR /app

EXPOSE 5005
EXPOSE 9101

LABEL org.opencontainers.image.title="flame" org.opencontainers.image.description="Flame - Self-hosted start page" org.opencontainers.image.vendor="pawelmalak" org.opencontainers.image.source="https://github.com/pawelmalak/flame" sovereign.image.tier="3" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/flame"]
