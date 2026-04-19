# =============================================================================
# SOVEREIGN HARDENED MIMIR
# Generated from template - Version: 2.13.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.13.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/grafana/mimir/releases/download/mimir-2.13.0/mimir-linux-amd64-2.13.0.tar.gz" -o /mimir.tar.gz && \
    tar -xzf /mimir.tar.gz -C / && rm /mimir.tar.gz && chmod +x /mimir 2>/dev/null || \
    curl -fsSL "https://github.com/grafana/mimir/releases/download/mimir-2.13.0/mimir-linux-amd64-2.13.0.tar.gz" -o /mimir && chmod +x /mimir

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/mimir /var/cache/mimir

FROM scratch
COPY --from=downloader /mimir /mimir
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/mimir /var/log/mimir
COPY --from=builder /var/cache/mimir /var/cache/mimir
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/mimir", "--version"]
ENTRYPOINT ["/mimir"]
LABEL org.opencontainers.image.title="mimir" \
      org.opencontainers.image.version="2.13.0" \
      org.opencontainers.image.vendor="Grafana" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
