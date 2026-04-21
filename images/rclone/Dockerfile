# =============================================================================
# SOVEREIGN HARDENED RCLONE
# Generated from template - Version: 1.73.5
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.73.5
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/rclone/rclone/releases/download/v${VERSION}/rclone-v${VERSION}-linux-amd64.zip" -o /rclone.zip && \
    unzip /rclone.zip -d /tmp/rclone && mv /tmp/rclone/rclone-v${VERSION}-linux-amd64/rclone /rclone && rm -rf /rclone.zip /tmp/rclone && chmod +x /rclone

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
EXPOSE 5572
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/rclone", "version"]
ENTRYPOINT ["/rclone"]
LABEL org.opencontainers.image.title="rclone" \
      org.opencontainers.image.version="1.73.5" \
      org.opencontainers.image.vendor="Rclone" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
