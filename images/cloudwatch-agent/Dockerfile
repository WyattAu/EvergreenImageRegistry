ARG VERSION=latest

FROM amazon/cloudwatch-agent:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/cloudwatch-agent /var/cache/cloudwatch-agent /etc/cloudwatch-agent 2>/dev/null || true


FROM scratch
COPY --from=upstream /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent /amazon-cloudwatch-agent
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/cloudwatch-agent /var/log/cloudwatch-agent
COPY --from=builder /var/cache/cloudwatch-agent /var/cache/cloudwatch-agent
COPY --from=builder /etc/cloudwatch-agent /etc/cloudwatch-agent

WORKDIR /app

EXPOSE 25888 12789
EXPOSE 9101

LABEL org.opencontainers.image.title="cloudwatch-agent" org.opencontainers.image.version="1.300046.0" org.opencontainers.image.vendor="Amazon Web Services" org.opencontainers.image.description="AWS CloudWatch Agent for metrics and log collection" sovereign.image.tier="1" sovereign.constraint.nonroot="true" sovereign.constraint.scratch="true" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="3000ms" sovereign.hft.cpu-pins="4-5" sovereign.hft.cpu-pins-mode="exclusive" sovereign.hft.deploy-strategy="hft-stateful" sovereign.hft.pre-stop-hook="true" sovereign.hft.pre-stop-delay="5s" sovereign.hft.connection-drain="true" sovereign.hft.sched-policy="SCHED_OTHER"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/amazon-cloudwatch-agent"]
