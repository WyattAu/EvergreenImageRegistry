# =============================================================================
# SOVEREIGN HARDENED TYPESENSE
# Generated from template - Version: 27.1
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=27.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/typesense/typesense/releases/download/27.1/typesense-27.1-linux-amd64.tar.gz" -o /typesense-server.tar.gz && \
    tar -xzf /typesense-server.tar.gz -C / && rm /typesense-server.tar.gz && chmod +x /typesense-server 2>/dev/null || \
    curl -fsSL "https://github.com/typesense/typesense/releases/download/27.1/typesense-27.1-linux-amd64.tar.gz" -o /typesense-server && chmod +x /typesense-server

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/typesense-server /var/cache/typesense-server

FROM scratch
COPY --from=downloader /typesense-server /typesense-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/typesense-server /var/log/typesense-server
COPY --from=builder /var/cache/typesense-server /var/cache/typesense-server
USER 65534:65534
WORKDIR /app
EXPOSE 8108
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/typesense-server", "--version"]
ENTRYPOINT ["/typesense-server"]
LABEL org.opencontainers.image.title="typesense" \
      org.opencontainers.image.version="27.1" \
      org.opencontainers.image.vendor="Typesense" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
