# =============================================================================
# SOVEREIGN ALIAS - PROMTAIL-AGENT -> promtail
# Alias for images/promtail/
# =============================================================================

ARG VERSION=2.9.4
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/grafana/loki/releases/download/v${VERSION}/promtail-linux-amd64.zip" -o /promtail.zip && \
    unzip -o /promtail.zip -d /tmp && \
    chmod +x /tmp/promtail-linux-amd64 && \
    mv /tmp/promtail-linux-amd64 /promtail

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/promtail

FROM scratch
COPY --from=downloader /promtail /usr/bin/promtail
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/promtail /var/log/promtail
USER 65534:65534
EXPOSE 9080 3100
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/bin/promtail", "--version"]
ENTRYPOINT ["/usr/bin/promtail"]
LABEL org.opencontainers.image.title="promtail-agent" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.source="https://github.com/grafana/loki" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="logging" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
