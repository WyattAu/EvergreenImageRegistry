# =============================================================================
# SOVEREIGN HARDENED RCLONE
# Generated from template - Version: 1.67.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.67.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/rclone/rclone/releases/download/v1.67.0/rclone_1.67.0_linux_amd64.tar.gz" -o /rclone.tar.gz && \
    tar -xzf /rclone.tar.gz -C / && rm /rclone.tar.gz && chmod +x /rclone 2>/dev/null || \
    curl -fsSL "https://github.com/rclone/rclone/releases/download/v1.67.0/rclone_1.67.0_linux_amd64.tar.gz" -o /rclone && chmod +x /rclone

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/rclone /var/cache/rclone

FROM scratch
COPY --from=downloader /rclone /rclone
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/rclone /var/log/rclone
COPY --from=builder /var/cache/rclone /var/cache/rclone
USER 65534:65534
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/rclone", "version"]
ENTRYPOINT ["/rclone"]
LABEL org.opencontainers.image.title="rclone" \
      org.opencontainers.image.version="1.67.0" \
      org.opencontainers.image.vendor="Rclone" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
