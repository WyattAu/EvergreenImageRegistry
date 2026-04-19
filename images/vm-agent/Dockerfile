# =============================================================================
# SOVEREIGN HARDENED VM-AGENT
# Generated from template - Version: 1.103.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.103.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/1.103.0/vmagent-linux-amd64-1.103.0.tar.gz" -o /vmagent.tar.gz && \
    tar -xzf /vmagent.tar.gz -C / && rm /vmagent.tar.gz && chmod +x /vmagent 2>/dev/null || \
    curl -fsSL "https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/1.103.0/vmagent-linux-amd64-1.103.0.tar.gz" -o /vmagent && chmod +x /vmagent

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/vmagent /var/cache/vmagent

FROM scratch
COPY --from=downloader /vmagent /vmagent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vmagent /var/log/vmagent
COPY --from=builder /var/cache/vmagent /var/cache/vmagent
USER 65534:65534
WORKDIR /app
EXPOSE 8429
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/vmagent", "--version"]
ENTRYPOINT ["/vmagent"]
LABEL org.opencontainers.image.title="vm-agent" \
      org.opencontainers.image.version="1.103.0" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
