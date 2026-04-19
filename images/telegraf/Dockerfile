# =============================================================================
# SOVEREIGN HARDENED TELEGRAF
# Generated from template - Version: 1.32.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.32.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/influxdata/telegraf/releases/download/v1.32.0/telegraf-1.32.0_linux_amd64.tar.gz" -o /telegraf.tar.gz && \
    tar -xzf /telegraf.tar.gz -C / && rm /telegraf.tar.gz && chmod +x /telegraf 2>/dev/null || \
    curl -fsSL "https://github.com/influxdata/telegraf/releases/download/v1.32.0/telegraf-1.32.0_linux_amd64.tar.gz" -o /telegraf && chmod +x /telegraf

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/telegraf /var/cache/telegraf

FROM scratch
COPY --from=downloader /telegraf /telegraf
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/telegraf /var/log/telegraf
COPY --from=builder /var/cache/telegraf /var/cache/telegraf
USER 65534:65534
WORKDIR /app
EXPOSE 8086
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/telegraf", "--version"]
ENTRYPOINT ["/telegraf"]
LABEL org.opencontainers.image.title="telegraf" \
      org.opencontainers.image.version="1.32.0" \
      org.opencontainers.image.vendor="InfluxData" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
