# =============================================================================
# SOVEREIGN HARDENED GRAFANA
# Generated from template - Version: 11.0.0
# Constraint: distroless - minimal runtime, no shell, CVE-free
# Priority: scratch > distroless (2nd best) > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=11.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/grafana/grafana/releases/download/11.0.0/grafana-11.0.0.linux-amd64.tar.gz" -o /grafana.tar.gz && \
    tar -xzf /grafana.tar.gz -C / && rm /grafana.tar.gz && chmod +x /grafana

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/grafana /var/cache/grafana

FROM gcr.io/distroless/static:nonroot
COPY --from=downloader /grafana /grafana
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/grafana /var/log/grafana
COPY --from=builder /var/cache/grafana /var/cache/grafana
USER 65534:65534
WORKDIR /app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD grafana version 2>/dev/null || exit 1
ENTRYPOINT ["/grafana"]
LABEL org.opencontainers.image.title="grafana" \
      org.opencontainers.image.version="11.0.0" \
      org.opencontainers.image.vendor="Grafana" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distroless="true"
