
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.16.0
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/juanfont/headscale/releases/download/v0.16.0/headscale_0.16.0_linux_${TARGETARCH} -o /headscale.tar.gz && \
    echo "2c86ff30605d8c4ab69e18d941ccd3deb2bf298a8db17878d8f6535070cc8a7c  /headscale.tar.gz" | sha256sum -c ; [ -f /headscale.tar.gz ] && \
    [ -f /headscale.tar.gz ] && tar -xzf /headscale.tar.gz -C / && rm -f /headscale.tar.gz && chmod +x /headscale 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/juanfont/headscale/releases/download/v0.16.0/headscale_0.16.0_linux_${TARGETARCH} -o /headscale && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/headscale /var/cache/headscale 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /headscale /headscale
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/headscale /var/log/headscale
COPY --from=builder /var/cache/headscale /var/cache/headscale
USER 65532:65532
WORKDIR /app
EXPOSE 8080 443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="headscale" \
      org.opencontainers.image.description="Headscale - open source implementation of the Tailscale control server" \
      org.opencontainers.image.version="0.16.0" \
      org.opencontainers.image.vendor="Headscale" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/juanfont/headscale"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
