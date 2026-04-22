ARG VERSION=v1.30.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kube-apiserver" -o /kube-apiserver && \
    echo "VERIFY_FROM_K8S_SHA256  /kube-apiserver" | sha256sum -c - && \
    chmod +x /kube-apiserver && strip /kube-apiserver

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kube-apiserver /var/cache/kube-apiserver /var/lib/kube-apiserver

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=downloader /kube-apiserver /usr/local/bin/kube-apiserver
COPY --from=builder /app /app
COPY --from=builder /var/log/kube-apiserver /var/log/kube-apiserver
COPY --from=builder /var/cache/kube-apiserver /var/cache/kube-apiserver
COPY --from=builder /var/lib/kube-apiserver /var/lib/kube-apiserver
RUN useradd -r -u 65534 -g '' kube-apiserver 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 6443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["kube-apiserver", "--version"]
ENTRYPOINT ["kube-apiserver"]
LABEL org.opencontainers.image.title="kube-apiserver" \
      org.opencontainers.image.version="1.30.1" \
      org.opencontainers.image.vendor="Kubernetes" \
      org.opencontainers.image.description="Sovereign hardened kube-apiserver - Kubernetes API server" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s"
