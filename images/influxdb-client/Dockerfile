# =============================================================================
# SOVEREIGN HARDENED INFLUXDB-CLIENT
# Generated from template - Version: 2.7.5
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.7.5
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://dl.influxdata.com/influxdb/releases/influxdb2-client-${VERSION}-linux-amd64.tar.gz" -o /influx.tar.gz && \
    tar -xzf /influx.tar.gz -C / && rm /influx.tar.gz && chmod +x /influx 2>/dev/null || \
    curl -fsSL "https://dl.influxdata.com/influxdb/releases/influxdb2-client-${VERSION}-linux-amd64.tar.gz" -o /influx && chmod +x /influx

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/influx /var/cache/influx

FROM scratch
COPY --from=downloader /influx /influx
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/influx /var/log/influx
COPY --from=builder /var/cache/influx /var/cache/influx
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
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
