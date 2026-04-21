# =============================================================================
# SOVEREIGN HARDENED INFLUXDB CLIENT
# Generated from template - Version: 2.7.5
# CLI tool for InfluxDB v2
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.7.5
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://dl.influxdata.com/influxdb/releases/influxdb2-client-2.7.5-linux-amd64.tar.gz" -o /influxdb-client.tar.gz && \
    tar -xzf /influxdb-client.tar.gz -C /tmp && rm /influxdb-client.tar.gz && \
    strip --strip-all /tmp/influxdb2-client-2.7.5/usr/bin/influx && \
    mv /tmp/influxdb2-client-2.7.5/usr/bin/influx /influx

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app

FROM scratch
COPY --from=downloader /influx /influx
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
USER 65534:65534
WORKDIR /app
EXPOSE 8086
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/influx", "version"]
ENTRYPOINT ["/influx"]
LABEL org.opencontainers.image.title="influxdb-client" \
      org.opencontainers.image.version="2.7.5" \
      org.opencontainers.image.vendor="InfluxData" \
      sovereign.image.tier="1" \
      sovereign.image.category="tsdb-client" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
