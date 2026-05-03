ARG VERSION=latest

FROM ghcr.io/vmware-tanzu/tweed:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
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

LABEL org.opencontainers.image.title="tweed" org.opencontainers.image.version="0.1.0" org.opencontainers.image.vendor="VMware Tanzu" org.opencontainers.image.source="https://github.com/vmware-tanzu/tweed" org.opencontainers.image.description="VPN mesh networking tool" evergreen.image.tier="1" evergreen.image.category="networking" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/tweed"]
