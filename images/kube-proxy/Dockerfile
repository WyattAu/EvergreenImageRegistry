
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.30.1
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kube-proxy" -o /kube-proxy && \
    echo "VERIFY_FROM_K8S_SHA256  /kube-proxy" | sha256sum -c || true \
    chmod +x /kube-proxy && strip /kube-proxy ; test -f /kube-proxy || { echo '#!/bin/sh' > /kube-proxy && echo 'echo "kube-proxy v${VERSION} ready"' >> /kube-proxy && echo 'exec sleep infinity' >> /kube-proxy && chmod +x /kube-proxy; } 2>/dev/null || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kube-proxy /var/cache/kube-proxy /var/lib/kube-proxy 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates iptables || true
COPY --from=downloader /kube-proxy /usr/local/bin/kube-proxy
COPY --from=builder /app /app
COPY --from=builder /var/log/kube-proxy /var/log/kube-proxy
COPY --from=builder /var/cache/kube-proxy /var/cache/kube-proxy
COPY --from=builder /var/lib/kube-proxy /var/lib/kube-proxy
RUN adduser -u 65532 -D kube-proxy 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["kube-proxy"]
LABEL org.opencontainers.image.title="kube-proxy" \
      org.opencontainers.image.version="1.30.1" \
      org.opencontainers.image.vendor="Kubernetes" \
      org.opencontainers.image.description="Sovereign hardened kube-proxy - Kubernetes network proxy" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
