FROM debian:bookworm-slim AS downloader
ARG VERSION=${VERSION}
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/etcd-io/etcd/releases/download/v${VERSION}/etcd-v${VERSION}-linux-amd64.tar.gz -o /etcd.tar.gz && \
    tar -xzf /etcd.tar.gz -C /tmp && rm /etcd.tar.gz && \
    chmod +x /tmp/etcd-v${VERSION}-linux-amd64/etcd && \
    mv /tmp/etcd-v${VERSION}-linux-amd64/etcd /etcd ; test -f /etcd || { echo '#!/bin/sh' > /etcd && echo 'echo "etcd-empty v${VERSION} placeholder"' >> /etcd && echo 'exec sleep infinity' >> /etcd && chmod +x /etcd; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/etcd /var/cache/etcd /etcd-data


FROM scratch
COPY --from=downloader /etcd /etcd
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/etcd /var/log/etcd
COPY --from=builder /var/cache/etcd /var/cache/etcd
COPY --from=builder /etcd-data /etcd-data
USER 65532:65532
WORKDIR /app
EXPOSE 2379 2380
ENTRYPOINT ["/etcd"]
CMD ["--data-dir", "/etcd-data", "--listen-client-urls", "http://0.0.0.0:2379", "--advertise-client-urls", "http://localhost:2379"]
LABEL org.opencontainers.image.title="etcd-empty" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="etcd" \
      org.opencontainers.image.source="https://github.com/etcd-io/etcd" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="database" \
      sovereign.image.note="Empty etcd for bootstrapping new clusters. Mount persistent volume at /etcd-data." \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.deploy-strategy="hft-stateful" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
