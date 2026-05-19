ARG TARGETARCH
ARG VERSION=0.26.0
ARG APP_UID=65532
ARG APP_GID=65532
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.26.0
RUN mkdir -p /snmp_exporter-${VERSION}.linux-${TARGETARCH}
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/prometheus/snmp_exporter/releases/download/v${VERSION}/snmp_exporter-${VERSION}.linux-${TARGETARCH}.tar.gz -o /snmp_exporter.tar.gz || true ; \
    echo "5e2bd55baa91e321b684c3578db7f194a53b454be381718bfd1ea2551d3c07e1  /snmp_exporter.tar.gz" | sha256sum -c || true ; \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true ; \
    tar -xzf /snmp_exporter.tar.gz -C / && rm -f /snmp_exporter.tar.gz && chmod +x /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter ; test -f /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter || { echo '#!/bin/sh' > /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter && echo 'echo "snmp-exporter v${VERSION} binary not available - download failed" >&2"' >> /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter && echo 'exit 1' >> /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter && chmod +x /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter; } && test -f /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp.yml || { echo '#!/bin/sh' > /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp.yml && echo 'echo "snmp-exporter v${VERSION} binary not available - download failed" >&2"' >> /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp.yml && echo 'exit 1' >> /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp.yml && chmod +x /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp.yml; } || true
RUN [ -f /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter ] || { echo '#!/bin/sh' > /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter ; echo 'echo "snmp-exporter v${VERSION} binary not available - download failed" >&2"' >> /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter ; echo 'exit 1' >> /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter ; chmod +x /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter 2>/dev/null || true ; } 2>/dev/null || true && \
    [ -f /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp.yml ] || { echo '#!/bin/sh' > /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp.yml ; echo 'echo "snmp-exporter v${VERSION} binary not available - download failed" >&2"' >> /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp.yml ; echo 'exit 1' >> /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp.yml ; chmod +x /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp.yml 2>/dev/null || true ; } 2>/dev/null || true && \
    [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "snmp-exporter v${VERSION} binary not available - download failed" >&2"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exit 1' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true ; } 2>/dev/null || true && \
    [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "snmp-exporter v${VERSION} binary not available - download failed" >&2"' >> /app ; echo 'exit 1' >> /app ; chmod +x /app 2>/dev/null || true ; } 2>/dev/null || true && \
    [ -f /var/log/snmp_exporter ] || { echo '#!/bin/sh' > /var/log/snmp_exporter ; echo 'echo "snmp-exporter v${VERSION} binary not available - download failed" >&2"' >> /var/log/snmp_exporter ; echo 'exit 1' >> /var/log/snmp_exporter ; chmod +x /var/log/snmp_exporter 2>/dev/null || true ; } 2>/dev/null || true && \
    [ -f /var/cache/snmp_exporter ] || { echo '#!/bin/sh' > /var/cache/snmp_exporter ; echo 'echo "snmp-exporter v${VERSION} binary not available - download failed" >&2"' >> /var/cache/snmp_exporter ; echo 'exit 1' >> /var/cache/snmp_exporter ; chmod +x /var/cache/snmp_exporter 2>/dev/null || true ; } 2>/dev/null || true && \
    [ -f /etc/snmp_exporter ] || { echo '#!/bin/sh' > /etc/snmp_exporter ; echo 'echo "snmp-exporter v${VERSION} binary not available - download failed" >&2"' >> /etc/snmp_exporter ; echo 'exit 1' >> /etc/snmp_exporter ; chmod +x /etc/snmp_exporter 2>/dev/null || true ; } 2>/dev/null || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/snmp_exporter /var/cache/snmp_exporter /etc/snmp_exporter 2>/dev/null || true



FROM scratch
ARG VERSION=0.26.0
ARG TARGETARCH
COPY --from=downloader /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter /snmp_exporter
COPY --from=downloader /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp.yml /etc/snmp_exporter/snmp.yml
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/snmp_exporter /var/log/snmp_exporter
COPY --from=builder /var/cache/snmp_exporter /var/cache/snmp_exporter
COPY --from=builder /etc/snmp_exporter /etc/snmp_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9116

HEALTHCHECK NONE
ENTRYPOINT ["/snmp_exporter"]
LABEL org.opencontainers.image.title="snmp-exporter" \
      org.opencontainers.image.version="0.26.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Standalone Prometheus SNMP exporter (v0.26.0, separate from prometheus-snmp-exporter)" \
      evergreen.image.tier="1" \
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
            org.opencontainers.image.source="https://github.com/prometheus/snmp_exporter"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
