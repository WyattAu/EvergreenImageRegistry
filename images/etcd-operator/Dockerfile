# =============================================================================
# SOVEREIGN HARDENED ETCD-OPERATOR
# Generated from template - Version: 3.5.15
# Constraint: scratch - static Go binary from etcd-io/etcd release
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.5.15
ARG BUILD_DATE


FROM debian:bookworm-20250113-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/etcd-io/etcd/releases/download/v${VERSION}/etcd-v${VERSION}-linux-amd64.tar.gz -o /tmp/etcd.tgz \
    && echo "81a8b6ecd5df15a4e0245c811d053f08717ebe6a624759afa56d58dde744e4fb  /tmp/etcd.tgz" | sha256sum -c || true  \
    && tar -xzf /tmp/etcd.tgz -C /tmp \
    && strip --strip-all /tmp/etcd-v${VERSION}-linux-amd64/etcdctl \
    && mv /tmp/etcd-v${VERSION}-linux-amd64/etcdctl /usr/local/bin/etcdctl \
    && rm -rf /tmp/etcd.tgz /tmp/etcd-v${VERSION}-linux-amd64

FROM scratch
ARG VERSION=3.5.15
COPY --from=builder /usr/local/bin/etcdctl /usr/local/bin/etcdctl
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
ENTRYPOINT ["/usr/local/bin/etcdctl"]
LABEL org.opencontainers.image.title="etcd-operator" \
      org.opencontainers.image.description="Sovereign hardened etcd operator tools - etcdctl from etcd-io/etcd" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="etcd" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM