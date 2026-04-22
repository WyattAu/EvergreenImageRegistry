# =============================================================================
# SOVEREIGN HARDENED PHOTOVIEW
# Generated from template - Version: 2.4.1
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.4.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/photoview/photoview/releases/download/v2.4.1/photoview_2.4.1_linux_amd64.tar.gz" -o /photoview.tar.gz && \
    tar -xzf /photoview.tar.gz -C / && rm /photoview.tar.gz && chmod +x /photoview 2>/dev/null || \
    curl -fsSL "https://github.com/photoview/photoview/releases/download/v2.4.1/photoview_2.4.1_linux_amd64.tar.gz" -o /photoview && chmod +x /photoview

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/photoview /var/cache/photoview

FROM scratch
COPY --from=downloader /photoview /photoview
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/photoview /var/log/photoview
COPY --from=builder /var/cache/photoview /var/cache/photoview
USER 65534:65534
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:80/api/v1/status"]
ENTRYPOINT ["/photoview"]
LABEL org.opencontainers.image.title="photoview" \
      org.opencontainers.image.version="2.4.1" \
      org.opencontainers.image.vendor="photoview/photoview" \
      org.opencontainers.image.source="https://github.com/photoview/photoview/releases/download/v2.4.1" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
