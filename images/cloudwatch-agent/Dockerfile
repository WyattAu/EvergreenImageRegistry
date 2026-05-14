ARG VERSION=1.300066.1
ARG TARGETARCH

FROM amazon/cloudwatch-agent:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
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

LABEL org.opencontainers.image.title="cloudwatch-agent" org.opencontainers.image.version="1.300046.0" org.opencontainers.image.vendor="Amazon Web Services" org.opencontainers.image.description="AWS CloudWatch Agent for metrics and log collection" evergreen.image.tier="1" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms" evergreen.hft.cpu-pins="4-5" evergreen.hft.cpu-pins-mode="exclusive" evergreen.hft.deploy-strategy="hft-stateful" evergreen.hft.pre-stop-hook="true" evergreen.hft.pre-stop-delay="5s" evergreen.hft.connection-drain="true" evergreen.hft.sched-policy="SCHED_OTHER" \
      org.opencontainers.image.source="https://github.com/aws/amazon-cloudwatch-agent"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/amazon-cloudwatch-agent"]
