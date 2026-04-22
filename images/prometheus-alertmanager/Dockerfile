# =============================================================================
# SOVEREIGN HARDENED PROMETHEUS-ALERTMANAGER
# Generated from template - Version: 0.27.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.27.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus/alertmanager/releases/download/v0.27.0/alertmanager-0.27.0.linux-amd64.tar.gz" -o /alertmanager.tar.gz && \
    echo "7ca6de06b30e930833fd88f608973d996b0c4a08e9fd9f4f6f91ceab8f6c5f23  /alertmanager.tar.gz" | sha256sum -c - && \
    tar -xzf /alertmanager.tar.gz -C / && rm /alertmanager.tar.gz && chmod +x /alertmanager 2>/dev/null || \
    curl -fsSL "https://github.com/prometheus/alertmanager/releases/download/v0.27.0/alertmanager-0.27.0.linux-amd64.tar.gz" -o /alertmanager && chmod +x /alertmanager

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/alertmanager /var/cache/alertmanager

FROM scratch
COPY --from=downloader /alertmanager /alertmanager
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/alertmanager /var/log/alertmanager
COPY --from=builder /var/cache/alertmanager /var/cache/alertmanager
USER 65532:65532
WORKDIR /app
EXPOSE 9093
ENTRYPOINT ["/alertmanager"]
LABEL org.opencontainers.image.title="prometheus-alertmanager" \
      org.opencontainers.image.version="0.27.0" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="6-7" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM