# =============================================================================
# SOVEREIGN HARDENED MIMIR
# Generated from template - Version: 2.10.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.10.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/grafana/mimir/releases/download/mimir-2.10.0/mimir_2.10.0_linux_amd64.tar.gz" -o /mimir.tar.gz && \
    tar -xzf /mimir.tar.gz -C /tmp && rm /mimir.tar.gz && \
    strip --strip-all /tmp/mimir-linux-amd64 && \
    mv /tmp/mimir-linux-amd64 /mimir

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/mimir /var/cache/mimir

FROM scratch
COPY --from=downloader /mimir /mimir
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/mimir /var/log/mimir
COPY --from=builder /var/cache/mimir /var/cache/mimir
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/mimir"]
LABEL org.opencontainers.image.title="mimir" \
      org.opencontainers.image.version="2.10.0" \
      org.opencontainers.image.vendor="Grafana" \
      sovereign.image.tier="1" \
      sovereign.image.category="tsdb" \
      sovereign.image.status="functional" \
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