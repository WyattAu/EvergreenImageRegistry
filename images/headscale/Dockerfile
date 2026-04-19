# =============================================================================
# SOVEREIGN HARDENED HEADSCALE
# Generated from template - Version: 0.16.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.16.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/juanfont/headscale/releases/download/v0.16.0/headscale_0.16.0_linux_amd64" -o /headscale.tar.gz && \
    tar -xzf /headscale.tar.gz -C / && rm /headscale.tar.gz && chmod +x /headscale 2>/dev/null || \
    curl -fsSL "https://github.com/juanfont/headscale/releases/download/v0.16.0/headscale_0.16.0_linux_amd64" -o /headscale && chmod +x /headscale

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/headscale /var/cache/headscale

FROM scratch
COPY --from=downloader /headscale /headscale
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/headscale /var/log/headscale
COPY --from=builder /var/cache/headscale /var/cache/headscale
USER 65534:65534
WORKDIR /app
EXPOSE 8080 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD headscale headscale --version
ENTRYPOINT ["/headscale"]
LABEL org.opencontainers.image.title="headscale" \
      org.opencontainers.image.version="0.16.0" \
      org.opencontainers.image.vendor="Headscale" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
