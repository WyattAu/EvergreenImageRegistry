# =============================================================================
# SOVEREIGN HARDENED MILVUS-MINIO
# Generated from template - Version: 2024.11.07
# Constraint: reference - Milvus minio sidecar (wolfi base)
# =============================================================================

ARG VERSION=2024.11.07
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates curl && || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.min.io/server/minio/release/linux-amd64/minio" -o /usr/local/bin/minio && \
    chmod +x /usr/local/bin/minio && \
    apk del curl
USER 65532:65532
EXPOSE 9000
ENTRYPOINT ["/usr/local/bin/minio"]
LABEL org.opencontainers.image.title="milvus-minio" \
      org.opencontainers.image.version="2024.11.07" \
      org.opencontainers.image.vendor="minio/minio" \
      org.opencontainers.image.description="Milvus minio sidecar - delegates to minio" \
      sovereign.image.tier="3" \
      sovereign.image.status="reference" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
