
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.58.0
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://pkgs.tailscale.com/stable/tailscale_latest_${TARGETARCH}.tgz" -o /tailscale.tgz ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://pkgs.tailscale.com/stable/tailscale_latest_${TARGETARCH}.tgz.sha256" -o /checksums.txt && \
    sha256sum -c /checksums.txt && \
    mkdir -p /tmp/tailscale ; \
    [ -f /tailscale.tgz ] && tar -xzf /tailscale.tgz -C /tmp/ ; \
    strip --strip-all /tmp/tailscale_${VERSION}_linux_${TARGETARCH}/tailscaled 2>/dev/null&& \
    strip --strip-all /tmp/tailscale_${VERSION}_linux_${TARGETARCH}/tailscale 2>/dev/null&& \
    mv /tmp/tailscale_${VERSION}_linux_${TARGETARCH}/tailscaled /tailscaled && \
    mv /tmp/tailscale_${VERSION}_linux_${TARGETARCH}/tailscale /tailscale && \
    rm -rf /tailscale.tgz /checksums.txt /tmp/* && { echo "Binary not available - download failed" >&2; exit 1; }
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /tailscaled /tailscaled
COPY --from=downloader /tailscale /tailscale
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 41641/udp

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:41641"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="tailscale" \
      org.opencontainers.image.description="tailscale container image" \
      org.opencontainers.image.version="1.58.0" \
      org.opencontainers.image.vendor="Tailscale" \
      org.opencontainers.image.source="https://github.com/tailscale/tailscale" \
      evergreen.image.tier="1" \
      evergreen.image.category="networking" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
