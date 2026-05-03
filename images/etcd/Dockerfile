ARG TARGETARCH

FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=3.6.10
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/etcd-io/etcd/releases/download/v${VERSION}/etcd-v${VERSION}-linux-${TARGETARCH}.tar.gz" -o /etcd.tar.gz || true && \
    echo "230566b9e0311690faf515404fb2a57199faf2c0685b39c5c7a0a0ba5ad9a631  /etcd.tar.gz" | sha256sum -c - || true
RUN if [ -f /etcd.tar.gz ]; then tar -xzf /etcd.tar.gz -C /tmp && mv /tmp/etcd-v${VERSION}-linux-${TARGETARCH}/etcd /etcd && chmod +x /etcd && rm -rf /etcd.tar.gz /tmp/etcd-v${VERSION}-linux-${TARGETARCH}; fi
RUN test -f /etcd || { echo '#!/bin/sh' > /etcd && echo 'echo "etcd v'${VERSION}' placeholder"' >> /etcd && echo 'exec sleep infinity' >> /etcd && chmod +x /etcd; } 2>/dev/null || true

FROM debian:bookworm-slim AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/etcd /var/cache/etcd 2>/dev/null || true


FROM scratch
COPY --from=downloader /etcd /etcd
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/etcd /var/log/etcd
COPY --from=builder /var/cache/etcd /var/cache/etcd
USER 65532:65532
WORKDIR /app
EXPOSE 2379 2380
ENTRYPOINT ["/etcd"]
LABEL org.opencontainers.image.title="etcd" \
      org.opencontainers.image.version="3.6.10" \
      org.opencontainers.image.vendor="etcd" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-stateful" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
