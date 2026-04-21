# =============================================================================
# SOVEREIGN HARDENED CLOUDWATCH AGENT
# Version: 1.300046.0
# Constraint: scratch - purest form, no shell, no package manager
# =============================================================================

ARG VERSION=1.300046.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/aws/cloudwatch-agent/releases/download/v${VERSION}/amazon-cloudwatch-agent-linux-amd64.tar.gz" -o /cwagent.tar.gz && \
    tar -xzf /cwagent.tar.gz -C / && rm /cwagent.tar.gz && chmod +x /amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/cloudwatch-agent /var/cache/cloudwatch-agent /etc/cloudwatch-agent

FROM scratch
COPY --from=downloader /amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent /amazon-cloudwatch-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/cloudwatch-agent /var/log/cloudwatch-agent
COPY --from=builder /var/cache/cloudwatch-agent /var/cache/cloudwatch-agent
COPY --from=builder /etc/cloudwatch-agent /etc/cloudwatch-agent
USER 65534:65534
WORKDIR /app
EXPOSE 25888 12789
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/amazon-cloudwatch-agent", "--version"]
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
