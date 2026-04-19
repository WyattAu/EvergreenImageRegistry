# =============================================================================
# SOVEREIGN HARDENED MEILISEARCH
# Generated from template - Version: 1.7.3
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.7.3
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/meilisearch/meilisearch/releases/download/v1.7.3/meilisearch-1.7.3-linux-amd64.tar.gz" -o /meilisearch.tar.gz && \
    tar -xzf /meilisearch.tar.gz -C / && rm /meilisearch.tar.gz && chmod +x /meilisearch 2>/dev/null || \
    curl -fsSL "https://github.com/meilisearch/meilisearch/releases/download/v1.7.3/meilisearch-1.7.3-linux-amd64.tar.gz" -o /meilisearch && chmod +x /meilisearch

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/meilisearch /var/cache/meilisearch

FROM scratch
COPY --from=downloader /meilisearch /meilisearch
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/meilisearch /var/log/meilisearch
COPY --from=builder /var/cache/meilisearch /var/cache/meilisearch
USER 65534:65534
WORKDIR /app
EXPOSE 7700
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/meilisearch", "--version"]
ENTRYPOINT ["/meilisearch"]
LABEL org.opencontainers.image.title="meilisearch" \
      org.opencontainers.image.version="1.7.3" \
      org.opencontainers.image.vendor="Meilisearch" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
