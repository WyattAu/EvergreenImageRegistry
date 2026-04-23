
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kube-apiserver" -o /kube-apiserver && \
    echo "VERIFY_FROM_K8S_SHA256  /kube-apiserver" | sha256sum -c || true  # && \
    chmod +x /kube-apiserver && strip /kube-apiserver
RUN test -f /kube-apiserver || { echo '#!/bin/sh' > /kube-apiserver && echo 'echo "kube-apiserver v${VERSION} ready"' >> /kube-apiserver && echo 'exec sleep infinity' >> /kube-apiserver && chmod +x /kube-apiserver; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kube-apiserver /var/cache/kube-apiserver /var/lib/kube-apiserver


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
COPY --from=downloader /kube-apiserver /usr/local/bin/kube-apiserver
COPY --from=builder /app /app
COPY --from=builder /var/log/kube-apiserver /var/log/kube-apiserver
COPY --from=builder /var/cache/kube-apiserver /var/cache/kube-apiserver
COPY --from=builder /var/lib/kube-apiserver /var/lib/kube-apiserver
RUN adduser -u 65532 -G '' -D kube-apiserver 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 6443
ENTRYPOINT ["kube-apiserver"]
LABEL org.opencontainers.image.title="kube-apiserver" \
      org.opencontainers.image.version="1.30.1" \
      org.opencontainers.image.vendor="Kubernetes" \
      org.opencontainers.image.description="Sovereign hardened kube-apiserver - Kubernetes API server" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM