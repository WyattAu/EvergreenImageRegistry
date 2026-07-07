
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.3.0

FROM ghcr.io/wyattau/evergreenimageregistry/mirror-debian-f9c6a2fd2ddb:latest AS downloader
ARG VERSION=2.7.6
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/caddyserver/caddy/releases/download/v2.7.6/caddy_2.7.6_linux_${TARGETARCH}.tar.gz -o /caddy.tar.gz && \
    echo "99587cf77c595f0bf62cc23c9ea101f9879fa016c7b689d498ce054904821f22  /caddy.tar.gz" | sha256sum -c ; [ -f /caddy.tar.gz ] && \
    [ -f /caddy.tar.gz ] && tar -xzf /caddy.tar.gz -C / && rm -f /caddy.tar.gz && chmod +x /caddy 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/caddyserver/caddy/releases/download/v2.7.6/caddy_2.7.6_linux_${TARGETARCH}.tar.gz -o /caddy || { echo "Binary not available - download failed" >&2; exit 1; }
FROM ghcr.io/wyattau/evergreenimageregistry/mirror-debian-f9c6a2fd2ddb:latest AS builder
RUN mkdir -p /app /var/log/caddy /var/cache/caddy 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim

COPY --from=downloader /caddy /caddy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/caddy /var/log/caddy
COPY --from=builder /var/cache/caddy /var/cache/caddy
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 80 443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/caddy"]
LABEL org.opencontainers.image.title="caddy-reverseproxy" \
      org.opencontainers.image.description="caddy-reverseproxy container image" \
      org.opencontainers.image.version="2.7.6" \
      org.opencontainers.image.vendor="Caddy" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="0-1" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-rolling" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
            org.opencontainers.image.source="https://github.com/caddyserver/caddy"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
