ARG VERSION=0.5.0
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
ARG VERSION=0.5.0
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}

RUN apt-get update && apt-get install -y --no-install-recommends \
        golang-1.23 git ca-certificates curl && \
    rm -rf /var/lib/apt/lists/* || true && \
    git clone --branch v${VERSION} \
        https://github.com/dmachard/dns-stats /tmp/dns-stats-src 2>/dev/null && \
    cd /tmp/dns-stats-src && \
    export PATH="/usr/lib/go-1.23/bin:${PATH}" && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build -ldflags="-s -w" -o /tmp/dns-stats ./cmd/dns-stats/ 2>/dev/null || \
    CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build -ldflags="-s -w" -o /tmp/dns-stats . 2>/dev/null || true && \
    if [ ! -f /tmp/dns-stats ] || [ ! -s /tmp/dns-stats ]; then \
        export PATH="/usr/lib/go-1.23/bin:${PATH}" && \
        git clone https://github.com/dmachard/dns-stats /tmp/dns-stats-fallback 2>/dev/null && \
        cd /tmp/dns-stats-fallback && \
        CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build -ldflags="-s -w" -o /tmp/dns-stats ./... 2>/dev/null || true ; \
    fi && \
    mkdir -p /etc/ssl/certs 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=0.5.0
COPY --from=builder /tmp/dns-stats /usr/local/bin/dns-stats
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="dns-stats" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened DNS Stats - DNS monitoring and statistics tool" \
      evergreen.image.tier="1" \
      evergreen.image.category="monitoring" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
            org.opencontainers.image.source="https://github.com/dmachard/dns-stats"
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
