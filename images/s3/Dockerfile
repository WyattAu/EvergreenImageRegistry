# =============================================================================
# SOVEREIGN HARDENED S3
# Generated from template - Version: 2024.5.28
# =============================================================================

ARG VERSION=2024.5.28
ARG BUILD_DATE

FROM alpine:2024.5.28-alpine
RUN apk add --no-cache minio ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id minio 2>/dev/null || adduser -D -u 65534 minio
RUN mkdir -p /app /var/log/s3 /var/cache/s3 && chown -R minio:minio /app /var/log/s3 /var/cache/s3
USER minio:minio
WORKDIR /app
EXPOSE 9000 9001
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /minio/health/live
ENTRYPOINT ["minio"]
LABEL org.opencontainers.image.title="s3" \
      org.opencontainers.image.version="2024.5.28" \
      org.opencontainers.image.vendor="MinIO" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
