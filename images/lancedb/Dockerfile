# =============================================================================
# SOVEREIGN HARDENED LANCEDB
# Generated from template - Version: 0.6.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.6.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/lancedb/lancedb/releases/download/v0.6.0/lancedb-0.6.0-x86_64-unknown-linux-gnu.tar.gz" -o /lancedb.tar.gz && \
    tar -xzf /lancedb.tar.gz -C / && rm /lancedb.tar.gz && chmod +x /lancedb 2>/dev/null || \
    curl -fsSL "https://github.com/lancedb/lancedb/releases/download/v0.6.0/lancedb-0.6.0-x86_64-unknown-linux-gnu.tar.gz" -o /lancedb && chmod +x /lancedb

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/lancedb /var/cache/lancedb

FROM scratch
COPY --from=downloader /lancedb /lancedb
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/lancedb /var/log/lancedb
COPY --from=builder /var/cache/lancedb /var/cache/lancedb
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD lancedb lancedb --version
ENTRYPOINT ["/lancedb"]
LABEL org.opencontainers.image.title="lancedb" \
      org.opencontainers.image.version="0.6.0" \
      org.opencontainers.image.vendor="LanceDB" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
