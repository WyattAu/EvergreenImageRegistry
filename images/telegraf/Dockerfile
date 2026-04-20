# =============================================================================
# SOVEREIGN HARDENED TELEGRAF
# Generated from template - 1.38.3
# Constraint: debian-slim with InfluxData apt repo (no pre-built tar.gz releases)
# =============================================================================

ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends gnupg2 curl ca-certificates && \
    curl -s https://repos.influxdata.com/influxdata-archive_compat.key | gpg --dearmor > /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg && \
    echo "deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main" > /etc/apt/sources.list.d/influxdata.list && \
    apt-get update && apt-get install -y --no-install-recommends telegraf && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/telegraf /var/cache/telegraf
USER 65534:65534
WORKDIR /app
EXPOSE 8086
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["telegraf", "--version"]
ENTRYPOINT ["telegraf"]
LABEL org.opencontainers.image.title="telegraf" \
      org.opencontainers.image.vendor="InfluxData" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
