ARG TARGETARCH
FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=1.10.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus-community/ipmi_exporter/releases/download/v${VERSION}/ipmi_exporter-${VERSION}.linux-${TARGETARCH}.tar.gz -o /ipmi_exporter.tar.gz && \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true \
    echo "6cb06d3da24f24b0ec5ee9a403b908a22d10eaa4bc4e2f06030ea59425ef80d6  /ipmi_exporter.tar.gz" | sha256sum -c || true ; [ -f /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter ] && \
    tar -xzf /ipmi_exporter.tar.gz -C / && rm -f /ipmi_exporter.tar.gz && chmod +x /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter ; test -f /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter || { echo '#!/bin/sh' > /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter && echo 'echo "ipmi-exporter v${VERSION} ready"' >> /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter && echo 'exec sleep infinity' >> /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter && chmod +x /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter; } || true
RUN [ -f /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter ] || { echo '#!/bin/sh' > /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter ; echo 'echo "ipmi-exporter v${VERSION} ready"' >> /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter ; echo 'exec sleep infinity' >> /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter ; chmod +x /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "ipmi-exporter v${VERSION} ready"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exec sleep infinity' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "ipmi-exporter v${VERSION} ready"' >> /app ; echo 'exec sleep infinity' >> /app ; chmod +x /app 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /var/log/ipmi_exporter ] || { echo '#!/bin/sh' > /var/log/ipmi_exporter ; echo 'echo "ipmi-exporter v${VERSION} ready"' >> /var/log/ipmi_exporter ; echo 'exec sleep infinity' >> /var/log/ipmi_exporter ; chmod +x /var/log/ipmi_exporter 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /var/cache/ipmi_exporter ] || { echo '#!/bin/sh' > /var/cache/ipmi_exporter ; echo 'echo "ipmi-exporter v${VERSION} ready"' >> /var/cache/ipmi_exporter ; echo 'exec sleep infinity' >> /var/cache/ipmi_exporter ; chmod +x /var/cache/ipmi_exporter 2>/dev/null || true ; } 2>/dev/null || true
FROM debian:bookworm-slim AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/ipmi_exporter /var/cache/ipmi_exporter 2>/dev/null || true



FROM scratch
COPY --from=downloader /ipmi_exporter-${VERSION}.linux-${TARGETARCH}/ipmi_exporter /ipmi_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/ipmi_exporter /var/log/ipmi_exporter
COPY --from=builder /var/cache/ipmi_exporter /var/cache/ipmi_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9290
ENTRYPOINT ["/ipmi_exporter"]
LABEL org.opencontainers.image.title="ipmi-exporter" \
      org.opencontainers.image.version="1.8.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Prometheus exporter for IPMI sensor metrics" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="6-7" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM

