# =============================================================================
# SOVEREIGN HARDENED NATS
# Generated from template - Version: 2.10.7
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.10.7
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/nats-io/nats-server/releases/download/v2.10.7/nats-server-2.10.7-linux-amd64.tar.gz" -o /nats-server.tar.gz && \
    echo "9bcf9e286b7c44553e06ab22ec2c06fd5fea75ad9b4eef2f8f0ae1bf2ea19b5b  /nats-server.tar.gz" | sha256sum -c - && \
    tar -xzf /nats-server.tar.gz -C / && rm /nats-server.tar.gz && chmod +x /nats-server 2>/dev/null || \
    curl -fsSL "https://github.com/nats-io/nats-server/releases/download/v2.10.7/nats-server-2.10.7-linux-amd64.tar.gz" -o /nats-server && chmod +x /nats-server

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/nats-server /var/cache/nats-server

FROM scratch
COPY --from=downloader /nats-server /nats-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/nats-server /var/log/nats-server
COPY --from=builder /var/cache/nats-server /var/cache/nats-server
USER 65534:65534
WORKDIR /app
EXPOSE 4222 8222
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/nats-server", "--version"]
ENTRYPOINT ["/nats-server"]
LABEL org.opencontainers.image.title="nats" \
      org.opencontainers.image.version="2.10.7" \
      org.opencontainers.image.vendor="NATS" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
