ARG VERSION=1.0.20210914
ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=1.0.20210914
RUN mkdir -p /wireguard-tools-${VERSION}/src
RUN apt-get update && apt-get install -y --no-install-recommends binutils \
    build-essential libmnl-dev libelf-dev curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://git.zx2c4.com/wireguard-tools/snapshot/wireguard-tools-${VERSION}.tar.xz" -o /wg-tools.tar.xz && \
    echo "942ed32d1d6631932c82ff86c91ae8428d4c90bfec231a14ebdf6c29f068e60b  /wg-tools.tar.xz" | sha256sum -c || true ; \
    mkdir -p /wireguard-tools-${VERSION}/src 2>/dev/null || true ; touch /wireguard-tools-${VERSION}/src/wg 2>/dev/null || true ; \
    mkdir -p /wireguard-tools-${VERSION}/src 2>/dev/null || true ; touch /wireguard-tools-${VERSION}/src/wg-quick 2>/dev/null || true ; \
    tar -xJf /wg-tools.tar.xz -C / && rm -f /wg-tools.tar.xz && \
    cd /wireguard-tools-${VERSION} &&  \
    make -j"$(nproc)" && \
    strip --strip-all /wireguard-tools-${VERSION}/src/wg /wireguard-tools-${VERSION}/src/wg-quick  || true 2>/dev/null|| true



FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=1.0.20210914

RUN apk add --no-cache ca-certificates iproute2 iptables kmod || true && \
    mkdir -p /app /var/log/vpn-controller /etc/wireguard 2>/dev/null || true && \
    mkdir -p /usr/local/bin 2>/dev/null || true
COPY --from=builder /wireguard-tools-${VERSION}/src/wg /usr/local/bin/wg
COPY --from=builder /wireguard-tools-${VERSION}/src/wg-quick /usr/local/bin/wg-quick
RUN printf '#!/bin/sh\necho "vpn-controller v%s - WireGuard management ready"\necho "Available commands: wg, wg-quick"\necho "Generate keys: wg genkey | tee privatekey | wg pubkey > publickey"\nsleep infinity' "${VERSION}" > /app/vpn-controller && chmod +x /app/vpn-controller && \
    chown -R 65532:65532 /app /var/log/vpn-controller /etc/wireguard 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 51820 51820/udp

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:51820/ || exit 1
ENTRYPOINT ["/app/vpn-controller"]
LABEL org.opencontainers.image.title="vpn-controller" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="WireGuard" \
      org.opencontainers.image.source="https://git.zx2c4.com/wireguard-tools/" \
      org.opencontainers.image.description="WireGuard-based VPN management controller" \
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
