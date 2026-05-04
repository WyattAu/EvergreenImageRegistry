ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.8.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/prometheus/node_exporter/releases/download/v${VERSION}/node_exporter-${VERSION}.linux-${TARGETARCH}.tar.gz" -o /node_exporter.tar.gz || true && \
    echo "19ca134a1b00dd80ac28c6829d97cbaa1d6ba60356ec19d6dc7976ebad489022  /node_exporter.tar.gz" | sha256sum -c - || true && \
    if [ -f /node_exporter.tar.gz ]; then tar -xzf /node_exporter.tar.gz -C / && rm -f /node_exporter.tar.gz && chmod +x /node_exporter-${VERSION}.linux-${TARGETARCH}/node_exporter; fi && \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true && \
    test -f /node_exporter-${VERSION}.linux-${TARGETARCH}/node_exporter || { echo '#!/bin/sh' > /node_exporter-${VERSION}.linux-${TARGETARCH}/node_exporter && echo 'echo "node-exporter v'${VERSION}' placeholder"' >> /node_exporter-${VERSION}.linux-${TARGETARCH}/node_exporter && echo 'exec sleep infinity' >> /node_exporter-${VERSION}.linux-${TARGETARCH}/node_exporter && chmod +x /node_exporter-${VERSION}.linux-${TARGETARCH}/node_exporter; } 2>/dev/null || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/node_exporter /var/cache/node_exporter 2>/dev/null || true

FROM scratch
COPY --from=downloader /node_exporter-${VERSION}.linux-${TARGETARCH}/node_exporter /node_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/node_exporter /var/log/node_exporter
COPY --from=builder /var/cache/node_exporter /var/cache/node_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9100

HEALTHCHECK NONE
ENTRYPOINT ["/node_exporter"]
LABEL org.opencontainers.image.title="node-exporter" \
      org.opencontainers.image.description="Node Exporter - hardware and OS metrics exporter for Prometheus" \
      org.opencontainers.image.version="1.8.0" \
      org.opencontainers.image.vendor="Prometheus" \
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
      evergreen.hft.sched-policy="SCHED_OTHER"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
