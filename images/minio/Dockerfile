# =============================================================================
# SOVEREIGN HARDENED MINIO
# Generated from template - Version: 2024.5.28
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=2024.5.28
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:2024.5.28
RUN apk add --no-cache minio ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 minio 2>/dev/null || true
RUN mkdir -p /app /var/log/minio /var/cache/minio && chown -R minio:minio /app /var/log/minio /var/cache/minio 2>/dev/null || true
USER minio:minio
WORKDIR /app
EXPOSE 9000 9001
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /minio/health/live
ENTRYPOINT ["minio"]
LABEL org.opencontainers.image.title="minio" \
      org.opencontainers.image.version="2024.5.28" \
      org.opencontainers.image.vendor="MinIO" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
