ARG VERSION=latest
ARG TARGETARCH

FROM ghcr.io/david415/wg-cloud:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
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

LABEL org.opencontainers.image.title="wg-cloud" org.opencontainers.image.version="0.1.0" org.opencontainers.image.vendor="WireGuard-Go-VPN" org.opencontainers.image.source="https://github.com/david415/WireGuard-Go-VPN" org.opencontainers.image.description="WireGuard cloud management plane" evergreen.image.tier="1" evergreen.image.category="networking" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/wg-cloud"]
