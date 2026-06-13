
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.39.0
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    TARGETVARIANT=$(case "${TARGETARCH}" in amd64) echo "x86_64";; arm64) echo "aarch64";; esac) && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/vectordotdev/vector/releases/download/v0.39.0/vector-0.39.0-${TARGETVARIANT}-unknown-linux-musl.tar.gz -o /vector.tar.gz && \
    echo "353c03537d506299a4f3635f495b505af7fb9188af2caf89014b8cdb2a2f39e1  /vector.tar.gz" | sha256sum -c ; [ -f /vector.tar.gz ] && \
    [ -f /vector.tar.gz ] && tar -xzf /vector.tar.gz -C / && rm -f /vector.tar.gz && chmod +x /vector 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/vectordotdev/vector/releases/download/v0.39.0/vector-0.39.0-${TARGETVARIANT}-unknown-linux-musl.tar.gz -o /vector && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/vector /var/cache/vector 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /vector /vector
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vector /var/log/vector
COPY --from=builder /var/cache/vector /var/cache/vector
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 9001

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9001"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="vector" \
      org.opencontainers.image.description="Vector - high-performance observability data pipeline" \
      org.opencontainers.image.version="0.39.0" \
      org.opencontainers.image.vendor="Vector" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/vectordotdev/vector"

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
