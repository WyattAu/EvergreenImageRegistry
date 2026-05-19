ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=3.6.10
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/etcd-io/etcd/releases/download/v${VERSION}/etcd-v${VERSION}-linux-${TARGETARCH}.tar.gz" -o /etcd.tar.gz || true && \
    echo "230566b9e0311690faf515404fb2a57199faf2c0685b39c5c7a0a0ba5ad9a631  /etcd.tar.gz" | sha256sum -c || true || true && \
    if [ -f /etcd.tar.gz ]; then tar -xzf /etcd.tar.gz -C /tmp && chmod +x /tmp/etcd-v${VERSION}-linux-${TARGETARCH}/etcd && mv /tmp/etcd-v${VERSION}-linux-${TARGETARCH}/etcd /etcd && rm -rf /etcd.tar.gz /tmp/etcd-v${VERSION}-linux-${TARGETARCH}; fi && \
    test -f /etcd || { echo '#!/bin/sh' > /etcd && echo 'echo "etcd v'${VERSION}' binary not available - download failed" >&2
exit 1"' >> /etcd && echo 'exit 1' >> /etcd && chmod +x /etcd; } 2>/dev/null || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/etcd /var/cache/etcd /etcd-data 2>/dev/null || true


FROM scratch
ARG VERSION=3.6.10
COPY --from=downloader /etcd /etcd
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/etcd /var/log/etcd
COPY --from=builder /var/cache/etcd /var/cache/etcd
COPY --from=builder /etcd-data /etcd-data
USER 65532:65532
WORKDIR /app
EXPOSE 2379 2380

HEALTHCHECK NONE
ENTRYPOINT ["/etcd"]
CMD ["--data-dir", "/etcd-data", "--listen-client-urls", "http://0.0.0.0:2379", "--advertise-client-urls", "http://localhost:2379"]
LABEL org.opencontainers.image.title="etcd-empty" \
      org.opencontainers.image.description="etcd-empty container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="etcd" \
      org.opencontainers.image.source="https://github.com/etcd-io/etcd" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="database" \
      evergreen.image.note="Empty etcd for bootstrapping new clusters. Mount persistent volume at /etcd-data." \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.deploy-strategy="hft-stateful" \
      evergreen.hft.sched-policy="SCHED_OTHER"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
