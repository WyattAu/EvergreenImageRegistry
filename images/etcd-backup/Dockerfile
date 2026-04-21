# =============================================================================
# SOVEREIGN HARDENED ETCD BACKUP
# Generated from template - Version: 3.5.15
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.5.15
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/etcd-io/etcd/releases/download/v${VERSION}/etcd-v${VERSION}-linux-amd64.tar.gz" -o etcd.tar.gz \
    && echo "81a8b6ecd5df15a4e0245c811d053f08717ebe6a624759afa56d58dde744e4fb  etcd.tar.gz" | sha256sum -c - \
    && tar -xzf etcd.tar.gz \
    && strip --strip-all etcd-v${VERSION}-linux-amd64/etcdctl \
    && mv etcd-v${VERSION}-linux-amd64/etcdctl /tmp/etcdctl

FROM scratch
COPY --from=builder /tmp/etcdctl /usr/local/bin/etcdctl
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /tmp
EXPOSE 2379
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/etcdctl", "version"]
ENTRYPOINT ["/usr/local/bin/etcdctl"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="backup" \
      org.opencontainers.image.title="etcd-backup" \
      org.opencontainers.image.description="Sovereign hardened etcd backup - etcdctl wrapper for etcd backup and restore operations" \
      org.opencontainers.image.version="${VERSION}"
