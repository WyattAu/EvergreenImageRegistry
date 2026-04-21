# =============================================================================
# SOVEREIGN HARDENED HEARTBEAT
# Version: 8.12.2
# Constraint: scratch - static Go binary, no shell, no package manager
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.12.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-${VERSION}-linux-x86_64.tar.gz" -o /heartbeat.tar.gz \
    && echo "0000000000000000000000000000000000000000000000000000000000000000  /heartbeat.tar.gz" | sha256sum -c - \
    && mkdir -p /opt/heartbeat \
    && tar -xzf /heartbeat.tar.gz -C /opt/heartbeat --strip-components=1 \
    && rm /heartbeat.tar.gz \
    && rm -rf /opt/heartbeat/kibana /opt/heartbeat/logs \
    && strip /opt/heartbeat/heartbeat || true \
    && chmod +x /opt/heartbeat/heartbeat

FROM debian:bookworm-slim AS builder
RUN mkdir -p /var/log/heartbeat /var/lib/heartbeat /var/cache/heartbeat

FROM scratch
COPY --from=downloader /opt/heartbeat /opt/heartbeat
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/heartbeat /var/log/heartbeat
COPY --from=builder /var/lib/heartbeat /var/lib/heartbeat
COPY --from=builder /var/cache/heartbeat /var/cache/heartbeat
USER 65534:65534
WORKDIR /opt/heartbeat
EXPOSE 5066
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/opt/heartbeat/heartbeat", "--version"]
ENTRYPOINT ["/opt/heartbeat/heartbeat"]
LABEL org.opencontainers.image.title="heartbeat" \
      org.opencontainers.image.description="Sovereign hardened Heartbeat - Elastic uptime monitor" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Elastic" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="observability" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
