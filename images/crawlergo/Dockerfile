# =============================================================================
# SOVEREIGN HARDENED CRAWLERGO
# Generated from template - Version: 0.4.4
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.4.4
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/Qianlitp/crawlergo/releases/download/v0.4.4/crawlergo_linux_amd64" -o /crawlergo.tar.gz && \
    tar -xzf /crawlergo.tar.gz -C / && rm /crawlergo.tar.gz && chmod +x /crawlergo 2>/dev/null || \
    curl -fsSL "https://github.com/Qianlitp/crawlergo/releases/download/v0.4.4/crawlergo_linux_amd64" -o /crawlergo && chmod +x /crawlergo

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/crawlergo /var/cache/crawlergo

FROM scratch
COPY --from=downloader /crawlergo /crawlergo
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/crawlergo /var/log/crawlergo
COPY --from=builder /var/cache/crawlergo /var/cache/crawlergo
USER 65534:65534
WORKDIR /app
EXPOSE 0
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/crawlergo", "--help"]
ENTRYPOINT ["/crawlergo"]
LABEL org.opencontainers.image.title="crawlergo" \
      org.opencontainers.image.version="0.4.4" \
      org.opencontainers.image.vendor="crawlergo" \
      org.opencontainers.image.source="https://github.com/Qianlitp/crawlergo/releases/download/v0.4.4" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
