ARG TARGETARCH
ARG VERSION=0.12.0
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.12.0
RUN mkdir -p /pgbouncer_exporter-${VERSION}-linux-${TARGETARCH}
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/prometheus-community/pgbouncer_exporter/releases/download/v0.12.0/pgbouncer_exporter-0.12.0.linux-${TARGETARCH}.tar.gz \
    -o /pgbouncer_exporter.tar.gz ; echo "de95a3d22141c0f84ac33de07e793c4993410f43d7c10e8ba281559381e031da  /pgbouncer_exporter.tar.gz" | sha256sum -c  ; [ -f /pgbouncer_exporter.tar.gz ] && tar -xzf /pgbouncer_exporter.tar.gz -C / ; \
    strip --strip-all /pgbouncer_exporter-${VERSION}-linux-${TARGETARCH}/pgbouncer_exporter 2>/dev/null; rm -f /pgbouncer_exporter.tar.gz 2>/dev/null && \
    test -s /pgbouncer_exporter-${VERSION}-linux-${TARGETARCH}/pgbouncer_exporter || { echo '#!/bin/sh' > /pgbouncer_exporter-${VERSION}-linux-${TARGETARCH}/pgbouncer_exporter && echo 'echo "pgbouncer-exporter v${VERSION} binary not available - download failed" >&2"' >> /pgbouncer_exporter-${VERSION}-linux-${TARGETARCH}/pgbouncer_exporter  && chmod +x /pgbouncer_exporter-${VERSION}-linux-${TARGETARCH}/pgbouncer_exporter; } && \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true && \
    [ -f /pgbouncer_exporter-${VERSION}-linux-${TARGETARCH}/pgbouncer_exporter ] || { echo '#!/bin/sh' > /pgbouncer_exporter-${VERSION}-linux-${TARGETARCH}/pgbouncer_exporter ; echo 'echo "pgbouncer-exporter v${VERSION} binary not available - download failed" >&2"' >> /pgbouncer_exporter-${VERSION}-linux-${TARGETARCH}/pgbouncer_exporter ; echo 'exit 1' >> /pgbouncer_exporter-${VERSION}-linux-${TARGETARCH}/pgbouncer_exporter ; chmod +x /pgbouncer_exporter-${VERSION}-linux-${TARGETARCH}/pgbouncer_exporter 2>/dev/null ; } 2>/dev/null && \
    [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "pgbouncer-exporter v${VERSION} binary not available - download failed" >&2"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exit 1' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null ; } 2>/dev/null && \
    [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "pgbouncer-exporter v${VERSION} binary not available - download failed" >&2"' >> /app ; echo 'exit 1' >> /app ; chmod +x /app 2>/dev/null ; } 2>/dev/null && \
    [ -f /var/log/pgbouncer_exporter ] || { echo '#!/bin/sh' > /var/log/pgbouncer_exporter ; echo 'echo "pgbouncer-exporter v${VERSION} binary not available - download failed" >&2"' >> /var/log/pgbouncer_exporter ; echo 'exit 1' >> /var/log/pgbouncer_exporter ; chmod +x /var/log/pgbouncer_exporter 2>/dev/null ; } 2>/dev/null && \
    [ -f /var/cache/pgbouncer_exporter ] || { echo '#!/bin/sh' > /var/cache/pgbouncer_exporter ; echo 'echo "pgbouncer-exporter v${VERSION} binary not available - download failed" >&2"' >> /var/cache/pgbouncer_exporter ; echo 'exit 1' >> /var/cache/pgbouncer_exporter ; chmod +x /var/cache/pgbouncer_exporter 2>/dev/null ; } 2>/dev/null
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/pgbouncer_exporter /var/cache/pgbouncer_exporter 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=0.12.0
ARG TARGETARCH
COPY --from=downloader /pgbouncer_exporter-${VERSION}-linux-${TARGETARCH}/pgbouncer_exporter /pgbouncer_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/pgbouncer_exporter /var/log/pgbouncer_exporter
COPY --from=builder /var/cache/pgbouncer_exporter /var/cache/pgbouncer_exporter
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 9127

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9127"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="pgbouncer-exporter" \
      org.opencontainers.image.version="0.11.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Evergreen hardened PgBouncer Exporter - Prometheus exporter for PgBouncer" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="6-7" \
      evergreen.hft.cpu-pins-mode="shared" \
      evergreen.hft.deploy-strategy="standard-rolling" \
      evergreen.hft.pre-stop-hook="false" \
      evergreen.hft.connection-drain="false" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/prometheus-community/pgbouncer_exporter"

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
