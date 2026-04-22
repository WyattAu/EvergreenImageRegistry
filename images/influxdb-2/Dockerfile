# =============================================================================
# SOVEREIGN HARDENED INFLUXDB-2
# Generated from template - Version: 2.7.5
# v2-only variant of InfluxDB
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.7.5
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://dl.influxdata.com/influxdb/releases/influxdb2-2.7.5-linux-amd64.tar.gz" -o /influxdb.tar.gz && \
    tar -xzf /influxdb.tar.gz -C /tmp && rm /influxdb.tar.gz && \
    strip --strip-all /tmp/influxdb2-2.7.5/usr/bin/influxd && \
    mv /tmp/influxdb2-2.7.5/usr/bin/influxd /influxd

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/lib/influxdb2 /var/log/influxdb2

FROM scratch
COPY --from=downloader /influxd /influxd
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/lib/influxdb2 /var/lib/influxdb2
COPY --from=builder /var/log/influxdb2 /var/log/influxdb2
USER 65532:65532
WORKDIR /app
EXPOSE 8086
ENTRYPOINT ["/influxd"]
LABEL org.opencontainers.image.title="influxdb-2" \
      org.opencontainers.image.version="2.7.5" \
      org.opencontainers.image.vendor="InfluxData" \
      org.opencontainers.image.description="InfluxDB v2-only variant for pure v2 API deployments" \
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