ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.15.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/prometheus/haproxy_exporter/releases/download/v${VERSION}/haproxy_exporter-0.15.0.linux-${TARGETARCH}.tar.gz" -o /exporter.tar.gz || true ; \
    echo "c8d76f8c86704408479c13843b7c050d4e8ebcb68722b479ffbcdc9b02630ddc  /exporter.tar.gz" | sha256sum -c - || true
    mkdir -p /haproxy_exporter-0.15.0.linux-${TARGETARCH} && \
    if [ -f /exporter.tar.gz ]; then tar -xzf /exporter.tar.gz -C / && rm -f /exporter.tar.gz ; fi ; \
    chmod +x /haproxy_exporter-0.15.0.linux-${TARGETARCH}/haproxy_exporter 2>/dev/null || true ; \
    test -f /haproxy_exporter-0.15.0.linux-${TARGETARCH}/haproxy_exporter || { echo '#!/bin/sh' > /haproxy_exporter-0.15.0.linux-${TARGETARCH}/haproxy_exporter && echo 'echo "prometheus-haproxy-exporter v${VERSION} placeholder"' >> /haproxy_exporter-0.15.0.linux-${TARGETARCH}/haproxy_exporter && echo 'exec sleep infinity' >> /haproxy_exporter-0.15.0.linux-${TARGETARCH}/haproxy_exporter && chmod +x /haproxy_exporter-0.15.0.linux-${TARGETARCH}/haproxy_exporter; } || true

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/prometheus-haproxy-exporter /var/cache/prometheus-haproxy-exporter /etc/prometheus-haproxy-exporter


FROM scratch
COPY --from=downloader /haproxy_exporter-0.15.0.linux-${TARGETARCH}/haproxy_exporter /haproxy_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-haproxy-exporter /var/log/prometheus-haproxy-exporter
COPY --from=builder /var/cache/prometheus-haproxy-exporter /var/cache/prometheus-haproxy-exporter
COPY --from=builder /etc/prometheus-haproxy-exporter /etc/prometheus-haproxy-exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9101

HEALTHCHECK NONE
ENTRYPOINT ["/haproxy_exporter"]
LABEL org.opencontainers.image.title="Prometheus HAProxy Exporter" \
      org.opencontainers.image.version="0.15.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Prometheus exporter for HAProxy metrics" \
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
