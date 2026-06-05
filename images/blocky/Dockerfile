
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.29.0
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    TARGETVARIANT=$(case "${TARGETARCH}" in amd64) echo "x86_64";; arm64) echo "arm64";; esac) && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/0xERR0R/blocky/releases/download/v0.29.0/blocky_v0.29.0_Linux_${TARGETVARIANT}.tar.gz -o /blocky.tar.gz ; \
    echo "ce70e5ef992a8eb980cf05e2902a63f9ee27296e1c69114d6dd6506549388428  /blocky.tar.gz" | sha256sum -c ; \
    [ -f /blocky.tar.gz ] && tar -xzf /blocky.tar.gz -C / && rm -f /blocky.tar.gz && chmod +x /blocky 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/0xERR0R/blocky/releases/download/v0.29.0/blocky_v0.29.0_Linux_${TARGETVARIANT}.tar.gz -o /blocky && { echo "Binary not available - download failed" >&2; exit 1; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/blocky /var/cache/blocky 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /blocky /blocky
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/blocky /var/log/blocky
COPY --from=builder /var/cache/blocky /var/cache/blocky
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 53 4000

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:53"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="blocky" \
      org.opencontainers.image.description="blocky container image" \
      org.opencontainers.image.version="0.29.0" \
      org.opencontainers.image.vendor="Blocky" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/0xERR0R/blocky"

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
