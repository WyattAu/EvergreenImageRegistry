ARG VERSION=v1.30.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kube-scheduler" -o /kube-scheduler && \
    echo "VERIFY_FROM_K8S_SHA256  /kube-scheduler" | sha256sum -c - && \
    chmod +x /kube-scheduler && strip /kube-scheduler

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kube-scheduler /var/cache/kube-scheduler /var/lib/kube-scheduler

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache ca-certificates
COPY --from=downloader /kube-scheduler /usr/local/bin/kube-scheduler
COPY --from=builder /app /app
COPY --from=builder /var/log/kube-scheduler /var/log/kube-scheduler
COPY --from=builder /var/cache/kube-scheduler /var/cache/kube-scheduler
COPY --from=builder /var/lib/kube-scheduler /var/lib/kube-scheduler
RUN useradd -r -u 65532 -g '' kube-scheduler 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["kube-scheduler"]
LABEL org.opencontainers.image.title="kube-scheduler" \
      org.opencontainers.image.version="1.30.1" \
      org.opencontainers.image.vendor="Kubernetes" \
      org.opencontainers.image.description="Sovereign hardened kube-scheduler - Kubernetes scheduler" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM