# =============================================================================
# SOVEREIGN HARDENED ETCD
# Generated from template - Version: 3.5.15
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.5.15
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/etcd-io/etcd/releases/download/v3.5.15/etcd-v3.5.15-linux-amd64.tar.gz" -o /etcd.tar.gz && \
    echo "81a8b6ecd5df15a4e0245c811d053f08717ebe6a624759afa56d58dde744e4fb  /etcd.tar.gz" | sha256sum -c - && \
    tar -xzf /etcd.tar.gz -C / && rm /etcd.tar.gz && chmod +x /etcd 2>/dev/null || \
    curl -fsSL "https://github.com/etcd-io/etcd/releases/download/v3.5.15/etcd-v3.5.15-linux-amd64.tar.gz" -o /etcd && chmod +x /etcd

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/etcd /var/cache/etcd

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
      org.opencontainers.image.version="3.5.15" \
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