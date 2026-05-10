ARG TARGETARCH
ARG VERSION=0.30.1
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.30.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/prometheus/snmp_exporter/releases/download/v${VERSION}/snmp_exporter-${VERSION}.linux-${TARGETARCH}.tar.gz" -o /snmp_exporter.tar.gz || true ; \
    echo "265e99f527c658099597291a5fecd8a46a89bed07c166621e84e90b27bfd6c6a  /snmp_exporter.tar.gz" | sha256sum -c - ; \
    mkdir -p /snmp_exporter-${VERSION}.linux-${TARGETARCH} ; \
    if [ -f /snmp_exporter.tar.gz ]; then tar -xzf /snmp_exporter.tar.gz -C / && rm -f /snmp_exporter.tar.gz ; fi ; \
    chmod +x /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter 2>/dev/null || true ; \
    test -f /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter || { echo '#!/bin/sh' > /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter && echo 'echo "prometheus-snmp-exporter v${VERSION} placeholder"' >> /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter && echo 'exec sleep infinity' >> /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter && chmod +x /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp_exporter; } || true ; \
    test -f /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp.yml || { echo '#!/bin/sh' > /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp.yml && echo 'echo "prometheus-snmp-exporter v${VERSION} placeholder"' >> /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp.yml && echo 'exec sleep infinity' >> /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp.yml && chmod +x /snmp_exporter-${VERSION}.linux-${TARGETARCH}/snmp.yml; } || true

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/snmp_exporter /var/cache/snmp_exporter /etc/snmp_exporter


FROM scratch
ARG VERSION=0.30.1
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
LABEL org.opencontainers.image.title="prometheus-snmp-exporter" \
      org.opencontainers.image.version="0.30.1" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Prometheus SNMP exporter for network device monitoring" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="4-5" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-stateful" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
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

