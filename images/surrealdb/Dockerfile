# =============================================================================
# SOVEREIGN HARDENED SURREALDB
# Generated from template - Version: 1.1.1
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.1.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/surrealdb/surrealdb/releases/download/v1.1.1/surrealdb-1.1.1-linux-amd64.tar.gz" -o /surreal.tar.gz && \
    tar -xzf /surreal.tar.gz -C / && rm /surreal.tar.gz && chmod +x /surreal 2>/dev/null || \
    curl -fsSL "https://github.com/surrealdb/surrealdb/releases/download/v1.1.1/surrealdb-1.1.1-linux-amd64.tar.gz" -o /surreal && chmod +x /surreal

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/surreal /var/cache/surreal

FROM scratch
COPY --from=downloader /surreal /surreal
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/surreal /var/log/surreal
COPY --from=builder /var/cache/surreal /var/cache/surreal
USER 65534:65534
WORKDIR /app
EXPOSE 8000 8001
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/surreal", "version"]
ENTRYPOINT ["/surreal"]
LABEL org.opencontainers.image.title="surrealdb" \
      org.opencontainers.image.version="1.1.1" \
      org.opencontainers.image.vendor="Surrealdb" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
