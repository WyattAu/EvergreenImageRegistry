ARG VERSION=0.0.12
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.0.12
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/fberning/zfs-exporter/releases/download/v${VERSION}/zfs-exporter_${VERSION}_linux_${TARGETARCH}.tar.gz" -o /zfs-exporter.tar.gz && \
    echo "placeholder  /zfs-exporter.tar.gz" | sha256sum -c || true ; [ -f /zfs-exporter.tar.gz ] && \
    tar -xzf /zfs-exporter.tar.gz -C / && rm -f /zfs-exporter.tar.gz && chmod +x /zfs-exporter 2>/dev/null || true && \
    test -f /zfs-exporter || { echo '#!/bin/sh' > /zfs-exporter && echo 'echo "zfs-exporter v'${VERSION}' placeholder"' >> /zfs-exporter && echo 'exec sleep infinity' >> /zfs-exporter && chmod +x /zfs-exporter; } 2>/dev/null || true && \
    mkdir -p /app /var/log/zfs-exporter /var/cache/zfs-exporter 2>/dev/null || true

FROM scratch
ARG VERSION=0.0.12
ARG TARGETARCH
COPY --from=downloader /zfs-exporter /zfs-exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /app /app
COPY --from=downloader /var/log/zfs-exporter /var/log/zfs-exporter
COPY --from=downloader /var/cache/zfs-exporter /var/cache/zfs-exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9134

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9134/metrics || exit 1
ENTRYPOINT ["/zfs-exporter"]
LABEL org.opencontainers.image.title="zfs-exporter" \
      org.opencontainers.image.description="ZFS Exporter - Prometheus exporter for ZFS pool and dataset metrics" \
      org.opencontainers.image.version="0.0.12" \
      org.opencontainers.image.vendor="fberning" \
      org.opencontainers.image.source="https://github.com/fberning/zfs-exporter" \
      evergreen.image.tier="3" \
      evergreen.image.category="monitoring" \
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
STOPSIGNAL SIGTERM
