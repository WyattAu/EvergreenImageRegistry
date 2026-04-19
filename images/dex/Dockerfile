# =============================================================================
# SOVEREIGN HARDENED DEX
# Generated from template - Version: 2.40.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.40.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/dexidp/dex/releases/download/v2.40.0/dex-2.40.0-linux-amd64.tar.gz" -o /dex.tar.gz && \
    tar -xzf /dex.tar.gz -C / && rm /dex.tar.gz && chmod +x /dex 2>/dev/null || \
    curl -fsSL "https://github.com/dexidp/dex/releases/download/v2.40.0/dex-2.40.0-linux-amd64.tar.gz" -o /dex && chmod +x /dex

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/dex /var/cache/dex

FROM scratch
COPY --from=downloader /dex /dex
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/dex /var/log/dex
COPY --from=builder /var/cache/dex /var/cache/dex
USER 65534:65534
WORKDIR /app
EXPOSE 5556
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/dex", "version"]
ENTRYPOINT ["/dex"]
LABEL org.opencontainers.image.title="dex" \
      org.opencontainers.image.version="2.40.0" \
      org.opencontainers.image.vendor="Dex" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
