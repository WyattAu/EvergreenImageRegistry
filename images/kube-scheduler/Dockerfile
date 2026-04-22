ARG VERSION=v1.30.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kube-scheduler" -o /kube-scheduler && \
    echo "VERIFY_FROM_K8S_SHA256  /kube-scheduler" | sha256sum -c - && \
    chmod +x /kube-scheduler && strip /kube-scheduler

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kube-scheduler /var/cache/kube-scheduler /var/lib/kube-scheduler

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=downloader /kube-scheduler /usr/local/bin/kube-scheduler
COPY --from=builder /app /app
COPY --from=builder /var/log/kube-scheduler /var/log/kube-scheduler
COPY --from=builder /var/cache/kube-scheduler /var/cache/kube-scheduler
COPY --from=builder /var/lib/kube-scheduler /var/lib/kube-scheduler
RUN useradd -r -u 65534 -g '' kube-scheduler 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["kube-scheduler", "--version"]
ENTRYPOINT ["kube-scheduler"]
LABEL org.opencontainers.image.title="kube-scheduler" \
      org.opencontainers.image.version="1.30.1" \
      org.opencontainers.image.vendor="Kubernetes" \
      org.opencontainers.image.description="Sovereign hardened kube-scheduler - Kubernetes scheduler" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s"
