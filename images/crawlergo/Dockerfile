
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v2.0.0
FROM ghcr.io/wyattau/evergreenimageregistry/mirror-debian-f9c6a2fd2ddb:latest AS downloader
ARG VERSION=0.4.4
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/Qianlitp/crawlergo/releases/download/v0.4.4/crawlergo_linux_amd64 -o /crawlergo.tar.gz ; \
    echo "cdf072120615104423a9827dc4134953133a9113626286ab38e9de1e6160dd3b  /crawlergo.tar.gz" | sha256sum -c ; \
    [ -f /crawlergo.tar.gz ] && tar -xzf /crawlergo.tar.gz -C / && rm -f /crawlergo.tar.gz && chmod +x /crawlergo 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/Qianlitp/crawlergo/releases/download/v0.4.4/crawlergo_linux_amd64 -o /crawlergo || { echo "Binary not available - download failed" >&2; exit 1; }



FROM ghcr.io/wyattau/evergreenimageregistry/mirror-debian-f9c6a2fd2ddb:latest AS builder
RUN mkdir -p /app /var/log/crawlergo /var/cache/crawlergo 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /crawlergo /crawlergo
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/crawlergo /var/log/crawlergo
COPY --from=builder /var/cache/crawlergo /var/cache/crawlergo
USER 65532:65532
WORKDIR /app
EXPOSE 0

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/crawlergo"]
LABEL org.opencontainers.image.title="crawlergo" \
      org.opencontainers.image.description="crawlergo container image" \
      org.opencontainers.image.version="0.4.4" \
      org.opencontainers.image.vendor="crawlergo" \
      org.opencontainers.image.source="https://github.com/Qianlitp/crawlergo/releases/download/v0.4.4" \
      evergreen.image.tier="3" \
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
