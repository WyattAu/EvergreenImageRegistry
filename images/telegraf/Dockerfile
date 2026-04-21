# =============================================================================
# SOVEREIGN HARDENED TELEGRAF
# Generated from template - 1.38.3
# Constraint: debian-slim - binary download from InfluxData
# =============================================================================

ARG VERSION=1.38.3
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL -k "https://dl.influxdata.com/telegraf/releases/telegraf-${VERSION}_linux_amd64.tar.gz" -o /tmp/telegraf.tar.gz && \
    tar -xzf /tmp/telegraf.tar.gz -C /opt && \
    rm -f /tmp/telegraf.tar.gz

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/telegraf /var/cache/telegraf
USER 65534:65534
WORKDIR /app
COPY --from=downloader /opt/telegraf* /opt/telegraf
ENV PATH="/opt/telegraf/usr/bin:${PATH}"
EXPOSE 8086
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/opt/telegraf/usr/bin/telegraf", "--version"]
ENTRYPOINT ["/opt/telegraf/usr/bin/telegraf"]
LABEL org.opencontainers.image.title="telegraf" \
      org.opencontainers.image.version="1.38.3" \
      org.opencontainers.image.vendor="InfluxData" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
