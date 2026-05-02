ARG VERSION=latest

FROM ghcr.io/vmware-tanzu/tweed:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/tweed /var/cache/tweed 2>/dev/null || true


FROM scratch
COPY --from=upstream /tweed /tweed
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/tweed /var/log/tweed
COPY --from=builder /var/cache/tweed /var/cache/tweed

WORKDIR /app

EXPOSE 9000 51820/udp
EXPOSE 9101

LABEL org.opencontainers.image.title="tweed" org.opencontainers.image.version="0.1.0" org.opencontainers.image.vendor="VMware Tanzu" org.opencontainers.image.source="https://github.com/vmware-tanzu/tweed" org.opencontainers.image.description="VPN mesh networking tool" sovereign.image.tier="1" sovereign.image.category="networking" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/tweed"]
