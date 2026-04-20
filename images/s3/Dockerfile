# =============================================================================
# SOVEREIGN HARDENED S3
# Generated from template - Version: RELEASE.2025-10-15T17-29-55Z
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=RELEASE.2025-10-15T17-29-55Z
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://dl.min.io/server/minio/release/linux-amd64/minio" -o /s3-server.tar.gz && \
    tar -xzf /s3-server.tar.gz -C / && rm /s3-server.tar.gz && chmod +x /s3-server 2>/dev/null || \
    curl -fsSL "https://dl.min.io/server/minio/release/linux-amd64/minio" -o /s3-server && chmod +x /s3-server

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/s3-server /var/cache/s3-server

FROM scratch
COPY --from=downloader /s3-server /s3-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/s3-server /var/log/s3-server
COPY --from=builder /var/cache/s3-server /var/cache/s3-server
USER 65534:65534
WORKDIR /app
EXPOSE 9000 9001
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/s3-server", "--version"]
ENTRYPOINT ["/s3-server"]
LABEL org.opencontainers.image.title="s3" \
      org.opencontainers.image.version="RELEASE.2025-10-15T17-29-55Z" \
      org.opencontainers.image.vendor="MinIO" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
