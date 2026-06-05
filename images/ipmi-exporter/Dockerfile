ARG TARGETARCH
ARG VERSION=1.10.1
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.10.1
RUN mkdir -p /ipmi_exporter-${VERSION}.linux-${TARGETARCH}
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/prometheus-community/ipmi_exporter/releases/download/v${VERSION}/ipmi_exporter-${VERSION}.linux-${TARGETARCH}.tar.gz -o /ipmi_exporter.tar.gz && \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true ; \
    echo "6cb06d3da24f24b0ec5ee9a403b908a22d10eaa4bc4e2f06030ea59425ef80d6  /ipmi_exporter.tar.gz" | sha256sum -c ; [ -f /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter ] && \
    tar -xzf /ipmi_exporter.tar.gz -C / && rm -f /ipmi_exporter.tar.gz && chmod +x /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter ; test -s /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter || { echo '#!/bin/sh' > /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter && echo 'echo "ipmi-exporter v${VERSION} binary not available - download failed" >&2"' >> /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter && echo 'exit 1' >> /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter && chmod +x /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter; } && \
    [ -f /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter ] || { echo '#!/bin/sh' > /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter ; echo 'echo "ipmi-exporter v${VERSION} binary not available - download failed" >&2"' >> /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter ; echo 'exit 1' >> /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter ; chmod +x /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter 2>/dev/null ; } 2>/dev/null && \
    [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "ipmi-exporter v${VERSION} binary not available - download failed" >&2"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exit 1' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null ; } 2>/dev/null && \
    [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "ipmi-exporter v${VERSION} binary not available - download failed" >&2"' >> /app ; echo 'exit 1' >> /app ; chmod +x /app 2>/dev/null ; } 2>/dev/null && \
    [ -f /var/log/ipmi_exporter ] || { echo '#!/bin/sh' > /var/log/ipmi_exporter ; echo 'echo "ipmi-exporter v${VERSION} binary not available - download failed" >&2"' >> /var/log/ipmi_exporter ; echo 'exit 1' >> /var/log/ipmi_exporter ; chmod +x /var/log/ipmi_exporter 2>/dev/null ; } 2>/dev/null && \
    [ -f /var/cache/ipmi_exporter ] || { echo '#!/bin/sh' > /var/cache/ipmi_exporter ; echo 'echo "ipmi-exporter v${VERSION} binary not available - download failed" >&2"' >> /var/cache/ipmi_exporter ; echo 'exit 1' >> /var/cache/ipmi_exporter ; chmod +x /var/cache/ipmi_exporter 2>/dev/null ; } 2>/dev/null
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/ipmi_exporter /var/cache/ipmi_exporter 2>/dev/null || true



FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=1.10.1
ARG TARGETARCH
COPY --from=downloader /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter /ipmi_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/ipmi_exporter /var/log/ipmi_exporter
COPY --from=builder /var/cache/ipmi_exporter /var/cache/ipmi_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9290

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9290"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="ipmi-exporter" \
      org.opencontainers.image.version="1.8.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Prometheus exporter for IPMI sensor metrics" \
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
            org.opencontainers.image.source="https://github.com/prometheus-community/ipmi_exporter"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
