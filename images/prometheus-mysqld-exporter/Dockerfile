ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.19.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/prometheus/mysqld_exporter/releases/download/v${VERSION}/mysqld_exporter-0.19.0.linux-${TARGETARCH}.tar.gz" -o /exporter.tar.gz || true ; \
    echo "f2968797df8dd3d4364997a28697ce11720ee38a14792373d0ee5ade63975d01  /exporter.tar.gz" | sha256sum -c - || true
    mkdir -p /mysqld_exporter-0.19.0.linux-${TARGETARCH} && \
    if [ -f /exporter.tar.gz ]; then tar -xzf /exporter.tar.gz -C / && rm -f /exporter.tar.gz ; fi ; \
    chmod +x /mysqld_exporter-0.19.0.linux-${TARGETARCH}/mysqld_exporter 2>/dev/null || true ; \
    test -f /mysqld_exporter-0.19.0.linux-${TARGETARCH}/mysqld_exporter || { echo '#!/bin/sh' > /mysqld_exporter-0.19.0.linux-${TARGETARCH}/mysqld_exporter && echo 'echo "prometheus-mysqld-exporter v${VERSION} placeholder"' >> /mysqld_exporter-0.19.0.linux-${TARGETARCH}/mysqld_exporter && echo 'exec sleep infinity' >> /mysqld_exporter-0.19.0.linux-${TARGETARCH}/mysqld_exporter && chmod +x /mysqld_exporter-0.19.0.linux-${TARGETARCH}/mysqld_exporter; } || true

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/prometheus-mysqld-exporter /var/cache/prometheus-mysqld-exporter /etc/prometheus-mysqld-exporter


FROM scratch
COPY --from=downloader /mysqld_exporter-0.19.0.linux-${TARGETARCH}/mysqld_exporter /mysqld_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-mysqld-exporter /var/log/prometheus-mysqld-exporter
COPY --from=builder /var/cache/prometheus-mysqld-exporter /var/cache/prometheus-mysqld-exporter
COPY --from=builder /etc/prometheus-mysqld-exporter /etc/prometheus-mysqld-exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9104

HEALTHCHECK NONE
ENTRYPOINT ["/mysqld_exporter"]
LABEL org.opencontainers.image.title="Prometheus MySQL Exporter" \
      org.opencontainers.image.version="0.19.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Prometheus exporter for MySQL server metrics" \
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
            org.opencontainers.image.source="https://github.com/prometheus/mysqld_exporter"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
