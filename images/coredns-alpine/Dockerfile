
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.11.1
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/coredns/coredns/releases/download/v${VERSION}/coredns_${VERSION}_linux_${TARGETARCH}.tgz -o /coredns.tar.gz ; \
    echo "f96cdee0934c5c12a28bb0fb080bed688fdd7bfdeae2f64984f02bdec2d65498  /coredns.tar.gz" | sha256sum -c ; \
    mkdir -p /tmp/coredns ; \
    [ -f /coredns.tar.gz ] && tar -xzf /coredns.tar.gz -C /tmp/coredns ; \
    strip --strip-all /tmp/coredns/coredns 2>/dev/null&& \
    mv /tmp/coredns/coredns /coredns && \
    rm -rf /coredns.tar.gz /tmp/* && { echo "Binary not available - download failed" >&2; exit 1; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/coredns /var/cache/coredns 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /coredns /coredns
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/coredns /var/log/coredns
COPY --from=builder /var/cache/coredns /var/cache/coredns
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 53 53/udp

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:53"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="coredns-alpine" \
      org.opencontainers.image.version="1.11.1" \
      org.opencontainers.image.vendor="CoreDNS" \
      org.opencontainers.image.source="https://github.com/coredns/coredns" \
      org.opencontainers.image.description="CoreDNS DNS server (alpine variant, built without Alpine)" \
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
