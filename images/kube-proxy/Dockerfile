ARG VERSION=v1.30.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kube-proxy" -o /kube-proxy && \
    echo "VERIFY_FROM_K8S_SHA256  /kube-proxy" | sha256sum -c - && \
    chmod +x /kube-proxy && strip /kube-proxy

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kube-proxy /var/cache/kube-proxy /var/lib/kube-proxy

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates iptables conntrack && rm -rf /var/lib/apt/lists/*
COPY --from=downloader /kube-proxy /usr/local/bin/kube-proxy
COPY --from=builder /app /app
COPY --from=builder /var/log/kube-proxy /var/log/kube-proxy
COPY --from=builder /var/cache/kube-proxy /var/cache/kube-proxy
COPY --from=builder /var/lib/kube-proxy /var/lib/kube-proxy
RUN useradd -r -u 65534 -g '' kube-proxy 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["kube-proxy", "--version"]
ENTRYPOINT ["kube-proxy"]
LABEL org.opencontainers.image.title="kube-proxy" \
      org.opencontainers.image.version="1.30.1" \
      org.opencontainers.image.vendor="Kubernetes" \
      org.opencontainers.image.description="Sovereign hardened kube-proxy - Kubernetes network proxy" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s"
