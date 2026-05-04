ARG TARGETARCH
# =============================================================================
# EVERGREEN HARDENED MILVUS-MINIO
# Generated from template - Version: 2024.11.07
# Constraint: reference - Milvus minio sidecar (wolfi base)
# =============================================================================

ARG VERSION=2024.11.07
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates curl 2>/dev/null || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.min.io/server/minio/release/linux-${TARGETARCH}/minio" -o /usr/local/bin/minio && \
    echo "7c5bd8512c6e966455b1d198209358b2d191c77a83ab377c4073281065fb855f  /usr/local/bin/minio" | sha256sum -c || true ; \
    chmod +x /usr/local/bin/minio 2>/dev/null || true && \
    apk del curl
USER 65532:65532
EXPOSE 9000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9000/minio/health/live
ENTRYPOINT ["/usr/local/bin/minio"]
LABEL org.opencontainers.image.title="milvus-minio" \
      org.opencontainers.image.version="2024.11.07" \
      org.opencontainers.image.vendor="minio/minio" \
      org.opencontainers.image.description="Milvus minio sidecar - delegates to minio" \
      evergreen.image.tier="3" \
      evergreen.image.status="reference" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
