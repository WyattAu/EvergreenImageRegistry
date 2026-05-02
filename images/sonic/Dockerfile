ARG VERSION=latest

FROM valeriansaliou/sonic:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/sonic /var/cache/sonic 2>/dev/null || true


FROM scratch
COPY --from=upstream /usr/local/bin/sonic /sonic
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/sonic /var/log/sonic
COPY --from=builder /var/cache/sonic /var/cache/sonic

WORKDIR /app

EXPOSE 1491
EXPOSE 9101

LABEL org.opencontainers.image.title="sonic" org.opencontainers.image.version="1.4.0" org.opencontainers.image.vendor="valeriansaliou" org.opencontainers.image.source="https://github.com/valeriansaliou/sonic" org.opencontainers.image.description="Fast, lightweight search backend" sovereign.image.tier="1" sovereign.image.category="search" sovereign.image.status="best-effort" sovereign.image.note="GNU binary may need glibc; fallback to debian-slim if scratch fails" sovereign.constraint.nonroot="true" sovereign.constraint.base="scratch" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="5s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/sonic"]
