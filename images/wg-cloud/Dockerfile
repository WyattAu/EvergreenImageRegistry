ARG VERSION=latest

FROM ghcr.io/david415/wg-cloud:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/wg-cloud /var/cache/wg-cloud 2>/dev/null || true


FROM scratch
COPY --from=upstream /wg-cloud /wg-cloud
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/wg-cloud /var/log/wg-cloud
COPY --from=builder /var/cache/wg-cloud /var/cache/wg-cloud

WORKDIR /app

EXPOSE 51820/udp 8080
EXPOSE 9101

LABEL org.opencontainers.image.title="wg-cloud" org.opencontainers.image.version="0.1.0" org.opencontainers.image.vendor="WireGuard-Go-VPN" org.opencontainers.image.source="https://github.com/david415/WireGuard-Go-VPN" org.opencontainers.image.description="WireGuard cloud management plane" sovereign.image.tier="1" sovereign.image.category="networking" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/wg-cloud"]
