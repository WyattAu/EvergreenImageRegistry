# =============================================================================
# SOVEREIGN HARDENED MINIO
# Generated from template - Version: 2024.5.28
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2024.5.28
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/minio/minio/releases/download/2024.5.28/minio-2024.5.28-linux-amd64" -o /minio.tar.gz && \
    tar -xzf /minio.tar.gz -C / && rm /minio.tar.gz && chmod +x /minio 2>/dev/null || \
    curl -fsSL "https://github.com/minio/minio/releases/download/2024.5.28/minio-2024.5.28-linux-amd64" -o /minio && chmod +x /minio

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/minio /var/cache/minio

FROM scratch
COPY --from=downloader /minio /minio
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/minio /var/log/minio
COPY --from=builder /var/cache/minio /var/cache/minio
USER 65534:65534
WORKDIR /app
EXPOSE 9000 9001
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/minio", "--version"]
ENTRYPOINT ["/minio"]
LABEL org.opencontainers.image.title="minio" \
      org.opencontainers.image.version="2024.5.28" \
      org.opencontainers.image.vendor="MinIO" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
