ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.5.4
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/ngoduykhanh/wireguard-ui/releases/download/v0.6.2/wireguard-ui-v0.6.2-linux-${TARGETARCH}.tar.gz -o /wireguard-ui.tar.gz ; \
    echo "2769536c2ef4cc3630b209675167afd5f199f4cc9f9f0d22ce492592dc1dc68d  /wireguard-ui.tar.gz" | sha256sum -c ; \
    mkdir -p /tmp/wireguard-ui ; \
    [ -f /wireguard-ui.tar.gz ] && tar -xzf /wireguard-ui.tar.gz -C /tmp/wireguard-ui/ ; \
    strip --strip-all /tmp/wireguard-ui/wireguard-ui 2>/dev/null&& \
    mv /tmp/wireguard-ui/wireguard-ui /wireguard-ui && \
    rm -rf /wireguard-ui.tar.gz /tmp/wireguard-ui && { echo "Binary not available - download failed" >&2; exit 1; }



FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim

COPY --from=downloader /wireguard-ui /wireguard-ui
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="wireguard-ui" \
      org.opencontainers.image.description="wireguard-ui container image" \
      org.opencontainers.image.version="0.5.4" \
      org.opencontainers.image.vendor="ngoduykhanh" \
      org.opencontainers.image.source="https://github.com/ngoduykhanh/wireguard-ui" \
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
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
