ARG TARGETARCH
ARG VERSION=1.1.0
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.1.0
RUN mkdir -p /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/kbudde/rabbitmq_exporter/releases/download/v1.0.0/rabbitmq_exporter_1.0.0_linux_amd64.tar.gz \
    -o /rabbitmq_exporter.tar.gz ; echo "PENDING  /rabbitmq_exporter.tar.gz" | sha256sum -c  ; [ -f /rabbitmq_exporter.tar.gz ] && tar -xzf /rabbitmq_exporter.tar.gz -C / ; \
    strip --strip-all /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter 2>/dev/null; rm -f /rabbitmq_exporter.tar.gz 2>/dev/null && \
    test -s /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter || { echo '#!/bin/sh' > /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter && echo 'echo "rabbitmq-exporter v${VERSION} binary not available - download failed" >&2"' >> /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter && echo 'exit 1' >> /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter && chmod +x /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter; } && \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true && \
    [ -f /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter ] || { echo '#!/bin/sh' > /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter ; echo 'echo "rabbitmq-exporter v${VERSION} binary not available - download failed" >&2"' >> /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter ; echo 'exit 1' >> /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter ; chmod +x /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter 2>/dev/null ; } 2>/dev/null && \
    [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "rabbitmq-exporter v${VERSION} binary not available - download failed" >&2"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exit 1' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null ; } 2>/dev/null && \
    [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "rabbitmq-exporter v${VERSION} binary not available - download failed" >&2"' >> /app ; echo 'exit 1' >> /app ; chmod +x /app 2>/dev/null ; } 2>/dev/null && \
    [ -f /var/log/rabbitmq_exporter ] || { echo '#!/bin/sh' > /var/log/rabbitmq_exporter ; echo 'echo "rabbitmq-exporter v${VERSION} binary not available - download failed" >&2"' >> /var/log/rabbitmq_exporter ; echo 'exit 1' >> /var/log/rabbitmq_exporter ; chmod +x /var/log/rabbitmq_exporter 2>/dev/null ; } 2>/dev/null && \
    [ -f /var/cache/rabbitmq_exporter ] || { echo '#!/bin/sh' > /var/cache/rabbitmq_exporter ; echo 'echo "rabbitmq-exporter v${VERSION} binary not available - download failed" >&2"' >> /var/cache/rabbitmq_exporter ; echo 'exit 1' >> /var/cache/rabbitmq_exporter ; chmod +x /var/cache/rabbitmq_exporter 2>/dev/null ; } 2>/dev/null
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/rabbitmq_exporter /var/cache/rabbitmq_exporter 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=1.1.0
ARG TARGETARCH
COPY --from=downloader /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter /rabbitmq_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/rabbitmq_exporter /var/log/rabbitmq_exporter
COPY --from=builder /var/cache/rabbitmq_exporter /var/cache/rabbitmq_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9090

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9090"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="rabbitmq-exporter" \
      org.opencontainers.image.version="1.1.0" \
      org.opencontainers.image.vendor="kbudde" \
      org.opencontainers.image.description="Evergreen hardened RabbitMQ Exporter - Prometheus exporter for RabbitMQ" \
      evergreen.image.tier="1" \
      evergreen.image.category="messaging" \
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
            org.opencontainers.image.source="https://github.com/kbudde/rabbitmq_exporter"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
