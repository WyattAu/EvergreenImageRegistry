ARG VERSION=latest

FROM ghcr.io/innernet-rs/innernet:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/innernet /var/cache/innernet 2>/dev/null || true


FROM scratch
COPY --from=upstream /usr/local/bin/innernet /innernet
COPY --from=upstream /usr/local/bin/innernet-serve /innernet-serve
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/innernet /var/log/innernet
COPY --from=builder /var/cache/innernet /var/cache/innernet

WORKDIR /app

EXPOSE 51820/udp
EXPOSE 9101

LABEL org.opencontainers.image.title="innernet" org.opencontainers.image.version="0.16.0" org.opencontainers.image.vendor="innernet-rs" org.opencontainers.image.source="https://github.com/innernet-rs/innernet" org.opencontainers.image.description="Private overlay network server (WireGuard-based)" sovereign.image.tier="1" sovereign.image.category="networking" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/innernet"]
