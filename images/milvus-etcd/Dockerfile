# =============================================================================
# EVERGREEN HARDENED MILVUS-ETCD
# Generated from template - Version: 3.5.17
# Constraint: reference - Milvus etcd sidecar (wolfi base)
# =============================================================================

ARG VERSION=3.5.17
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN apk add --no-cache etcd ca-certificates
USER 65532:65532
EXPOSE 2379 2380
LABEL org.opencontainers.image.title="milvus-etcd" \
      org.opencontainers.image.version="3.5.17" \
      org.opencontainers.image.vendor="etcd" \
      org.opencontainers.image.description="Milvus etcd sidecar - delegates to etcd" \
      evergreen.image.tier="3" \
      evergreen.image.status="reference" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/milvus-io/milvus"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:2379"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
