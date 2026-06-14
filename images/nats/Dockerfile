ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=2.12.7
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/nats-io/nats-server/releases/download/v2.12.7/nats-server-v2.12.7-linux-${TARGETARCH}.sbom.spdx.json -o /nats-server.tar.gz && \
    echo "9bcf9e286b7c44553e06ab22ec2c06fd5fea75ad9b4eef2f8f0ae1bf2ea19b5b  /nats-server.tar.gz" | sha256sum -c ; [ -f /nats-server.tar.gz ] && \
    [ -f /nats-server.tar.gz ] && tar -xzf /nats-server.tar.gz -C / && rm -f /nats-server.tar.gz && chmod +x /nats-server 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/nats-io/nats-server/releases/download/v2.12.7/nats-server-v2.12.7-linux-${TARGETARCH}.sbom.spdx.json -o /nats-server && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/nats-server /var/cache/nats-server 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim

COPY --from=downloader /nats-server /nats-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/nats-server /var/log/nats-server
COPY --from=builder /var/cache/nats-server /var/cache/nats-server
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 4222 8222

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:4222"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "nats-server"]
LABEL org.opencontainers.image.title="nats" \
      org.opencontainers.image.description="NATS - high-performance messaging system" \
      org.opencontainers.image.version="2.12.7" \
      org.opencontainers.image.vendor="NATS" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/nats-io/nats-server"

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
