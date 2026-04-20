# =============================================================================
# SOVEREIGN HARDENED FOCALBOARD
# Generated from template - Version: 8.0.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/mattermost/focalboard/releases/download/v7.8.0/focalboard-server-linux-amd64.tar.gz" -o /focalboard-server.tar.gz && \
    tar -xzf /focalboard-server.tar.gz -C / && rm /focalboard-server.tar.gz && chmod +x /focalboard-server 2>/dev/null || \
    curl -fsSL "https://github.com/mattermost/focalboard/releases/download/v7.8.0/focalboard-server-linux-amd64.tar.gz" -o /focalboard-server && chmod +x /focalboard-server

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/focalboard-server /var/cache/focalboard-server

FROM scratch
COPY --from=downloader /focalboard-server /focalboard-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/focalboard-server /var/log/focalboard-server
COPY --from=builder /var/cache/focalboard-server /var/cache/focalboard-server
USER 65534:65534
WORKDIR /app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/focalboard-server", "--version"]
ENTRYPOINT ["/focalboard-server"]
LABEL org.opencontainers.image.title="focalboard" \
      org.opencontainers.image.version="8.0.0" \
      org.opencontainers.image.vendor="Focalboard" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
