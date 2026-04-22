ARG VERSION=v1.30.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kube-controller-manager" -o /kube-controller-manager && \
    echo "VERIFY_FROM_K8S_SHA256  /kube-controller-manager" | sha256sum -c - && \
    chmod +x /kube-controller-manager && strip /kube-controller-manager

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kube-controller /var/cache/kube-controller /var/lib/kube-controller

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=downloader /kube-controller-manager /usr/local/bin/kube-controller-manager
COPY --from=builder /app /app
COPY --from=builder /var/log/kube-controller /var/log/kube-controller
COPY --from=builder /var/cache/kube-controller /var/cache/kube-controller
COPY --from=builder /var/lib/kube-controller /var/lib/kube-controller
RUN useradd -r -u 65534 -g '' kube-controller 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["kube-controller-manager", "--version"]
ENTRYPOINT ["kube-controller-manager"]
LABEL org.opencontainers.image.title="kube-controller" \
      org.opencontainers.image.version="1.30.1" \
      org.opencontainers.image.vendor="Kubernetes" \
      org.opencontainers.image.description="Sovereign hardened kube-controller - Kubernetes controller manager" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s"
