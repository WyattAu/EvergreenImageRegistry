# =============================================================================
# SOVEREIGN HARDENED QDRANT
# Generated from template - Version: 1.11.4
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.11.4
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/qdrant/qdrant/releases/download/v1.11.4/qdrant-1.11.4-x86_64-unknown-linux-musl.tar.gz" -o /qdrant.tar.gz && \
    tar -xzf /qdrant.tar.gz -C / && rm /qdrant.tar.gz && chmod +x /qdrant 2>/dev/null || \
    curl -fsSL "https://github.com/qdrant/qdrant/releases/download/v1.11.4/qdrant-1.11.4-x86_64-unknown-linux-musl.tar.gz" -o /qdrant && chmod +x /qdrant

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/qdrant /var/cache/qdrant

FROM scratch
COPY --from=downloader /qdrant /qdrant
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/qdrant /var/log/qdrant
COPY --from=builder /var/cache/qdrant /var/cache/qdrant
USER 65534:65534
WORKDIR /app
EXPOSE 6333 6334
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/qdrant", "--version"]
ENTRYPOINT ["/qdrant"]
LABEL org.opencontainers.image.title="qdrant" \
      org.opencontainers.image.version="1.11.4" \
      org.opencontainers.image.vendor="Qdrant" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
