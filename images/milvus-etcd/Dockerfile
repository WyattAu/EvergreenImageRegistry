# =============================================================================
# EVERGREEN HARDENED MILVUS-ETCD
# Generated from template - Version: 3.5.17
# Constraint: reference - Milvus etcd sidecar (wolfi base)
# =============================================================================

ARG VERSION=3.5.17
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache etcd ca-certificates || true
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
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD etcdctl endpoint health
ENTRYPOINT ["etcd"]
