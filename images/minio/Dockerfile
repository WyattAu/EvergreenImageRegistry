# =============================================================================
# SOVEREIGN HARDENED MINIO
# Generated from template - Version: 2024.5.28
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=2024.5.28
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends minio ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' minio 2>/dev/null || true
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
      sovereign.constraint.debian_slim="true"
