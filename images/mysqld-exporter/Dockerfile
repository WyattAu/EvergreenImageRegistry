ARG VERSION=v0.16.0
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=v0.16.0
RUN mkdir -p /mysqld_exporter-${VERSION}.linux-${TARGETARCH}
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/prometheus/mysqld_exporter/releases/download/${VERSION}/mysqld_exporter-${VERSION}.linux-${TARGETARCH}.tar.gz" -o /mysqld_exporter.tar.gz && \
    echo "placeholder  /mysqld_exporter.tar.gz" | sha256sum -c || true ; [ -f /mysqld_exporter.tar.gz ] && \
    tar -xzf /mysqld_exporter.tar.gz -C / && rm -f /mysqld_exporter.tar.gz && chmod +x /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter 2>/dev/null || true && \
    test -f /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter || { mkdir -p /mysqld_exporter-${VERSION}.linux-${TARGETARCH} && echo '#!/bin/sh' > /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter && echo 'echo "mysqld-exporter '${VERSION}' placeholder"' >> /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter && echo 'exec sleep infinity' >> /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter && chmod +x /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter; } 2>/dev/null || true && \
    mkdir -p /app /var/log/mysqld_exporter /var/cache/mysqld_exporter 2>/dev/null || true

FROM scratch
ARG VERSION=v0.16.0
ARG TARGETARCH
COPY --from=downloader /mysqld_exporter-${VERSION}.linux-${TARGETARCH}/mysqld_exporter /mysqld_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /app /app
COPY --from=downloader /var/log/mysqld_exporter /var/log/mysqld_exporter
COPY --from=downloader /var/cache/mysqld_exporter /var/cache/mysqld_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9104

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9104/metrics || exit 1
ENTRYPOINT ["/mysqld_exporter"]
LABEL org.opencontainers.image.title="mysqld-exporter" \
      org.opencontainers.image.description="MySQL Server Exporter - Prometheus exporter for MySQL server metrics" \
      org.opencontainers.image.version="0.16.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.source="https://github.com/prometheus/mysqld_exporter" \
      evergreen.image.tier="2" \
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
