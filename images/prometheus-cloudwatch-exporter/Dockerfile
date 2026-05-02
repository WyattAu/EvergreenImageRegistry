ARG VERSION=latest

FROM prom/cloudwatch-exporter:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/prometheus-cloudwatch-exporter /var/cache/prometheus-cloudwatch-exporter 2>/dev/null || true


FROM scratch
COPY --from=upstream /bin/cloudwatch_exporter /cloudwatch_exporter
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-cloudwatch-exporter /var/log/prometheus-cloudwatch-exporter
COPY --from=builder /var/cache/prometheus-cloudwatch-exporter /var/cache/prometheus-cloudwatch-exporter

WORKDIR /app

EXPOSE 9106
EXPOSE 9101

LABEL org.opencontainers.image.title="prometheus-cloudwatch-exporter" org.opencontainers.image.version="0.15.0" org.opencontainers.image.vendor="Prometheus Community" org.opencontainers.image.description="Prometheus exporter for AWS CloudWatch metrics" sovereign.image.tier="1" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="3000ms" sovereign.hft.cpu-pins="4-5" sovereign.hft.cpu-pins-mode="exclusive" sovereign.hft.deploy-strategy="hft-stateful" sovereign.hft.pre-stop-hook="true" sovereign.hft.pre-stop-delay="5s" sovereign.hft.connection-drain="true" sovereign.hft.sched-policy="SCHED_OTHER"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/cloudwatch_exporter"]
