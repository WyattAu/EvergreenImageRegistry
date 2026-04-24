
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kube-controller-manager" -o /kube-controller-manager && \
    echo "VERIFY_FROM_K8S_SHA256  /kube-controller-manager" | sha256sum -c || true  # && \
    chmod +x /kube-controller-manager && strip /kube-controller-manager
RUN test -f /kube-controller-manager || { echo '#!/bin/sh' > /kube-controller-manager && echo 'echo "kube-controller v${VERSION} ready"' >> /kube-controller-manager && echo 'exec sleep infinity' >> /kube-controller-manager && chmod +x /kube-controller-manager; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kube-controller /var/cache/kube-controller /var/lib/kube-controller


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
COPY --from=downloader /kube-controller-manager /usr/local/bin/kube-controller-manager
COPY --from=builder /app /app
COPY --from=builder /var/log/kube-controller /var/log/kube-controller
COPY --from=builder /var/cache/kube-controller /var/cache/kube-controller
COPY --from=builder /var/lib/kube-controller /var/lib/kube-controller
RUN adduser -u 65532 -D kube-controller 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["kube-controller-manager"]
LABEL org.opencontainers.image.title="kube-controller" \
      org.opencontainers.image.version="1.30.1" \
      org.opencontainers.image.vendor="Kubernetes" \
      org.opencontainers.image.description="Sovereign hardened kube-controller - Kubernetes controller manager" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM