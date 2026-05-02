ARG VERSION=latest

FROM ghcr.io/pawelmalak/flame:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/flame-ui /var/cache/flame-ui 2>/dev/null || true


FROM scratch
COPY --from=upstream /app/flame /usr/local/bin/flame
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/flame-ui /var/log/flame-ui
COPY --from=builder /var/cache/flame-ui /var/cache/flame-ui

WORKDIR /app

EXPOSE 5005
EXPOSE 9101

LABEL org.opencontainers.image.title="flame-ui" org.opencontainers.image.description="Flame - UI variant" org.opencontainers.image.vendor="pawelmalak" org.opencontainers.image.source="https://github.com/pawelmalak/flame" sovereign.image.tier="3" sovereign.constraint.nonroot="true" sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["flame"]

CMD ["--ui-only"]
