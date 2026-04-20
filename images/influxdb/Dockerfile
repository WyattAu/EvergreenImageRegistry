# =============================================================================
# SOVEREIGN HARDENED INFLUXDB
# Generated from template - Version: 2.7.7
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.7.7
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg2 && \
    curl -fsSL https://repos.influxdata.com/influxdata-archive_compat.key | gpg --dearmor -o /usr/share/keyrings/influxdb.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/influxdb.gpg] https://repos.influxdata.com/debian stable main" > /etc/apt/sources.list.d/influxdb.list && \
    apt-get update && apt-get install -y --no-install-recommends influxdb2 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' influxdb 2>/dev/null || true
RUN mkdir -p /app /var/log/influxd /var/cache/influxd && chown -R influxdb:influxdb /app /var/log/influxd /var/cache/influxd 2>/dev/null || true
USER influxdb
WORKDIR /app
EXPOSE 8086 9999
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8086/health
ENTRYPOINT ["influxd"]
LABEL org.opencontainers.image.title="influxdb" \
      org.opencontainers.image.version="2.7.7" \
      org.opencontainers.image.vendor="InfluxData" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
