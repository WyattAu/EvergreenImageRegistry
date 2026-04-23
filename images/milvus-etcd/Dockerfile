# =============================================================================
# SOVEREIGN HARDENED MILVUS-ETCD
# Generated from template - Version: 3.5.17
# Constraint: reference - Milvus etcd sidecar (wolfi base)
# =============================================================================

ARG VERSION=3.5.17
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache etcd ca-certificates
USER 65532:65532
EXPOSE 2379 2380
LABEL org.opencontainers.image.title="milvus-etcd" \
      org.opencontainers.image.version="3.5.17" \
      org.opencontainers.image.vendor="etcd" \
      org.opencontainers.image.description="Milvus etcd sidecar - delegates to etcd" \
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
