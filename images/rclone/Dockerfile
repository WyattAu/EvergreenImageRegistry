# =============================================================================
# SOVEREIGN HARDENED RCLONE
# Generated from template - Version: 1.67.0
# =============================================================================

ARG VERSION=1.67.0
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "https://github.com/rclone/rclone/releases/download/v1.67.0/rclone_1.67.0_linux_amd64.tar.gz" -o /rclone.tar.gz && \
    unzip -o /rclone.tar.gz && rm /rclone.tar.gz && chmod +x /rclone

FROM alpine:3.21 AS builder
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
    CMD /rclone version 2>/dev/null || exit 1
ENTRYPOINT ["/rclone"]
LABEL org.opencontainers.image.title="rclone" \
      org.opencontainers.image.version="1.67.0" \
      org.opencontainers.image.vendor="Rclone" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.static="true"