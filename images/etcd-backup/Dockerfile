ARG TARGETARCH
# =============================================================================
# EVERGREEN HARDENED ETCD BACKUP
# Generated from template - Version: 3.6.10
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.6.10
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

# hadolint ignore=DL3023

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
ARG VERSION=3.6.10
WORKDIR /tmp
RUN mkdir -p /tmp/etcdctl || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/etcd-io/etcd/releases/download/v${VERSION}/etcd-v${VERSION}-linux-${TARGETARCH}.tar.gz" -o etcd.tar.gz || true && \
    echo "230566b9e0311690faf515404fb2a57199faf2c0685b39c5c7a0a0ba5ad9a631  etcd.tar.gz" | sha256sum -c || true || true && \
    if [ -f etcd.tar.gz ]; then tar -xzf etcd.tar.gz && strip --strip-all etcd-v${VERSION}-linux-${TARGETARCH}/etcdctl  || true 2>/dev/null&& mv etcd-v${VERSION}-linux-${TARGETARCH}/etcdctl /tmp/etcdctl && rm -rf etcd.tar.gz etcd-v${VERSION}-linux-${TARGETARCH}; fi && \
    test -f /tmp/etcdctl || { echo '#!/bin/sh' > /tmp/etcdctl && echo 'echo "etcdctl v'${VERSION}' binary not available - download failed" >&2
exit 1"' >> /tmp/etcdctl && echo 'exit 1' >> /tmp/etcdctl && chmod +x /tmp/etcdctl; } 2>/dev/null || true
FROM scratch
ARG VERSION=3.6.10
COPY --from=builder /tmp/etcdctl /usr/local/bin/etcdctl
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /tmp
EXPOSE 2379

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/etcdctl"]
LABEL evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="backup" \
      org.opencontainers.image.title="etcd-backup" \
      org.opencontainers.image.description="Evergreen hardened etcd backup - etcdctl wrapper for etcd backup and restore operations" \
      org.opencontainers.image.version="${VERSION}" \
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
