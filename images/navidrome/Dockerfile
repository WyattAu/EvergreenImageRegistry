
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.52.5
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/navidrome/navidrome/releases/download/v0.52.5/navidrome_0.52.5_linux_${TARGETARCH}.tar.gz -o /navidrome.tar.gz && \
    echo "b9781ea560ea09926557c665472faa26920738a5ffa0680c19f70df97f51598f  /navidrome.tar.gz" | sha256sum -c ; [ -f /navidrome.tar.gz ] && \
    [ -f /navidrome.tar.gz ] && tar -xzf /navidrome.tar.gz -C / && rm -f /navidrome.tar.gz && chmod +x /navidrome 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/navidrome/navidrome/releases/download/v0.52.5/navidrome_0.52.5_linux_${TARGETARCH}.tar.gz -o /navidrome && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/navidrome /var/cache/navidrome 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /navidrome /navidrome
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/navidrome /var/log/navidrome
COPY --from=builder /var/cache/navidrome /var/cache/navidrome
USER 65532:65532
WORKDIR /app
EXPOSE 4533

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:4533"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="navidrome" \
      org.opencontainers.image.description="navidrome container image" \
      org.opencontainers.image.version="0.52.5" \
      org.opencontainers.image.vendor="Navidrome" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/navidrome/navidrome"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
