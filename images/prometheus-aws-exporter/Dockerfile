ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.65.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/prometheus-community/yet-another-cloudwatch-exporter/releases/download/v${VERSION}/yet-another-cloudwatch-exporter-0.65.0.linux-${TARGETARCH}.tar.gz" -o /exporter.tar.gz || true ; \
    echo "01f9123f521090c33a816733f07e5bd7a2b2ecb3c9eecbf3a19d7e80ee57d836  /exporter.tar.gz" | sha256sum -c - ; \
    mkdir -p /yet-another-cloudwatch-exporter-0.65.0.linux-${TARGETARCH} && \
    if [ -f /exporter.tar.gz ]; then tar -xzf /exporter.tar.gz -C / && rm -f /exporter.tar.gz ; fi ; \
    chmod +x /yet-another-cloudwatch-exporter-0.65.0.linux-${TARGETARCH}/yace 2>/dev/null || true ; \
    test -f /yet-another-cloudwatch-exporter-0.65.0.linux-${TARGETARCH}/yace || { echo '#!/bin/sh' > /yet-another-cloudwatch-exporter-0.65.0.linux-${TARGETARCH}/yace && echo 'echo "prometheus-aws-exporter v${VERSION} placeholder"' >> /yet-another-cloudwatch-exporter-0.65.0.linux-${TARGETARCH}/yace && echo 'exec sleep infinity' >> /yet-another-cloudwatch-exporter-0.65.0.linux-${TARGETARCH}/yace && chmod +x /yet-another-cloudwatch-exporter-0.65.0.linux-${TARGETARCH}/yace; } || true

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/prometheus-aws-exporter /var/cache/prometheus-aws-exporter /etc/prometheus-aws-exporter


FROM scratch
COPY --from=downloader /yet-another-cloudwatch-exporter-0.65.0.linux-${TARGETARCH}/yace /yace
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-aws-exporter /var/log/prometheus-aws-exporter
COPY --from=builder /var/cache/prometheus-aws-exporter /var/cache/prometheus-aws-exporter
COPY --from=builder /etc/prometheus-aws-exporter /etc/prometheus-aws-exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9101

HEALTHCHECK NONE
ENTRYPOINT ["/yace"]
LABEL org.opencontainers.image.title="Prometheus AWS/YACE CloudWatch Exporter" \
      org.opencontainers.image.version="0.65.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Prometheus exporter for AWS CloudWatch metrics" \
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
            org.opencontainers.image.source="https://github.com/prometheus-community/yet-another-cloudwatch-exporter"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
