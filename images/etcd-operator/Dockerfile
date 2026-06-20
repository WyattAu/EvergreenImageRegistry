ARG TARGETARCH
# =============================================================================
# EVERGREEN HARDENED ETCD-OPERATOR
# Generated from template - Version: 3.6.10
# Constraint: scratch - static Go binary from etcd-io/etcd release
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.6.10
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM debian@sha256:f70dc8d6a8b6a06824c92471a1a258030836b26b043881358b967bf73de7c5ab AS builder
ARG TARGETARCH
ARG VERSION=3.6.10
RUN mkdir -p /usr/local/bin/etcdctl || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/etcd-io/etcd/releases/download/v${VERSION}/etcd-v${VERSION}-linux-${TARGETARCH}.tar.gz" -o /tmp/etcd.tgz && \
    echo "230566b9e0311690faf515404fb2a57199faf2c0685b39c5c7a0a0ba5ad9a631  /tmp/etcd.tgz" | sha256sum -c && \
    if [ -f /tmp/etcd.tgz ]; then tar -xzf /tmp/etcd.tgz -C /tmp && strip --strip-all /tmp/etcd-v${VERSION}-linux-${TARGETARCH}/etcdctl 2>/dev/null&& mv /tmp/etcd-v${VERSION}-linux-${TARGETARCH}/etcdctl /usr/local/bin/etcdctl && rm -rf /tmp/etcd.tgz /tmp/etcd-v${VERSION}-linux-${TARGETARCH}; fi && \' && { echo "Binary not available - download failed" >&2; exit 1; }
ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
ARG VERSION=3.6.10
COPY --from=builder /usr/local/bin/etcdctl /usr/local/bin/etcdctl
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/etcdctl"]
LABEL org.opencontainers.image.title="etcd-operator" \
      org.opencontainers.image.description="Evergreen hardened etcd operator tools - etcdctl from etcd-io/etcd" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="etcd" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
            org.opencontainers.image.source="https://github.com/etcd-io/etcd"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
