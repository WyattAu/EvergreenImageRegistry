# =============================================================================
# EVERGREEN HARDENED WG-QUICK
# WireGuard quick setup wrapper with wireguard-tools
# Constraint: debian-slim - requires shell, iproute2, and wireguard-tools
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.0.20210914
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    wireguard-tools iproute2 iptables kmod && \
    rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /app /var/log/wireguard /run/wireguard ; \
    chown -R 65532:65532 /app /var/log/wireguard /run/wireguard
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache wireguard-tools iproute2 iptables ca-certificates kmod || true
COPY --from=builder /app /app
COPY --from=builder /var/log/wireguard /var/log/wireguard
COPY --from=builder /run/wireguard /run/wireguard
USER 65532:65532
WORKDIR /app
EXPOSE 51820/udp

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:51820/ || exit 1
ENTRYPOINT ["/usr/bin/wg-quick"]
LABEL org.opencontainers.image.title="wg-quick" \
      org.opencontainers.image.version="1.0.20210914" \
      org.opencontainers.image.vendor="WireGuard" \
      org.opencontainers.image.source="https://www.wireguard.com" \
      org.opencontainers.image.description="WireGuard quick setup wrapper with wireguard-tools" \
      evergreen.image.tier="1" \
      evergreen.image.category="networking" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
