# =============================================================================
# EVERGREEN HARDENED ZFS-EXPORTER
# wolfi-base (needs /dev/zfs kernel device - can't use scratch)
# =============================================================================
ARG VERSION=0.5.3
ARG SHIM_VERSION=v1.0.0

FROM golang:1.24-bookworm AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 --branch "v${VERSION}" https://github.com/frebib/zfs-exporter.git . || \
    git clone --depth 1 https://github.com/frebib/zfs-exporter.git .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags='-s -w' -o /zfs-exporter .

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=builder /zfs-exporter /usr/local/bin/zfs-exporter
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
RUN adduser -u 65532 -D exporter 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /
EXPOSE 9134 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--http", "127.0.0.1:9134/metrics"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/zfs-exporter"]
LABEL org.opencontainers.image.title="zfs-exporter" \
      org.opencontainers.image.description="ZFS statistics exporter for Prometheus" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="frebib" \
      org.opencontainers.image.source="https://github.com/frebib/zfs-exporter"
LABEL evergreen.base.image="wolfi" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGTERM
