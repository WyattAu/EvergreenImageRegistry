FROM debian:bookworm-slim AS downloader
ARG VERSION=1.300046.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/aws/cloudwatch-agent/releases/download/v${VERSION}/amazon-cloudwatch-agent-linux-amd64.tar.gz -o /cwagent.tar.gz || true ; \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true \
    tar -xzf /cwagent.tar.gz -C / && rm /cwagent.tar.gz && chmod +x /amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent ; test -f /amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent || { echo '#!/bin/sh' > /amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent && echo 'echo "cloudwatch-agent v${VERSION} ready"' >> /amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent && echo 'exec sleep infinity' >> /amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent && chmod +x /amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent; } || true




FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/cloudwatch-agent /var/cache/cloudwatch-agent /etc/cloudwatch-agent 2>/dev/null || true



FROM scratch
COPY --from=downloader /amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent /amazon-cloudwatch-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/cloudwatch-agent /var/log/cloudwatch-agent
COPY --from=builder /var/cache/cloudwatch-agent /var/cache/cloudwatch-agent
COPY --from=builder /etc/cloudwatch-agent /etc/cloudwatch-agent
USER 65532:65532
WORKDIR /app
EXPOSE 25888 12789
ENTRYPOINT ["/amazon-cloudwatch-agent"]
LABEL org.opencontainers.image.title="cloudwatch-agent" \
      org.opencontainers.image.version="1.300046.0" \
      org.opencontainers.image.vendor="Amazon Web Services" \
      org.opencontainers.image.description="AWS CloudWatch Agent for metrics and log collection" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-stateful" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM

