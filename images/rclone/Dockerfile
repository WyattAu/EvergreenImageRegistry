# =============================================================================
# SOVEREIGN HARDENED RCLONE
# Generated from template - Version: 1.67.0
# Constraint: distroless/static - no shell, no package manager
# =============================================================================

ARG VERSION=1.67.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "https://github.com/rclone/rclone/releases/download/v1.67.0/rclone_1.67.0_linux_amd64.zip" -o /rclone.tar.gz && \
    tar -xzf /rclone.tar.gz -C / && rm /rclone.tar.gz && chmod +x /rclone

FROM cgr.dev/chainguard/wolfi AS builder
RUN mkdir -p /app /var/log/rclone /var/cache/rclone

FROM gcr.io/distroless/static:nonroot
COPY --from=downloader /rclone /rclone
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/rclone /var/log/rclone
COPY --from=builder /var/cache/rclone /var/cache/rclone
USER 65534:65534
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD rclone --version 2>/dev/null || exit 1
ENTRYPOINT ["/rclone"]
LABEL org.opencontainers.image.title="rclone" \
      org.opencontainers.image.version="1.67.0" \
      org.opencontainers.image.vendor="Rclone" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distroless="true"
