# =============================================================================
# SOVEREIGN HARDENED MINIFLUX
# Generated from template - Version: 2.2.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.2.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/miniflux/miniflux/releases/download/v2.2.0/miniflux-2.2.0-linux-amd64.tar.gz" -o /miniflux.tar.gz && \
    tar -xzf /miniflux.tar.gz -C / && rm /miniflux.tar.gz && chmod +x /miniflux 2>/dev/null || \
    curl -fsSL "https://github.com/miniflux/miniflux/releases/download/v2.2.0/miniflux-2.2.0-linux-amd64.tar.gz" -o /miniflux && chmod +x /miniflux

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/miniflux /var/cache/miniflux

FROM scratch
COPY --from=downloader /miniflux /miniflux
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/miniflux /var/log/miniflux
COPY --from=builder /var/cache/miniflux /var/cache/miniflux
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/miniflux", "--version"]
ENTRYPOINT ["/miniflux"]
LABEL org.opencontainers.image.title="miniflux" \
      org.opencontainers.image.version="2.2.0" \
      org.opencontainers.image.vendor="Miniflux" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
