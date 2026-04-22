ARG VERSION=v1.69.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/rclone/rclone/releases/download/v1.69.1/rclone-v1.69.1-linux-amd64.zip" -o /rclone && chmod +x /rclone

FROM scratch
COPY --from=downloader /rclone /rclone
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 5572
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/rclone", "--version"]
ENTRYPOINT ["/rclone"]
LABEL org.opencontainers.image.title="rclone" \
      org.opencontainers.image.version="v1.69.1" \
      org.opencontainers.image.vendor="Rclone" \
      org.opencontainers.image.source="https://github.com/rclone/rclone" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
