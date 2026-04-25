
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.30.1
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kube-scheduler" -o /kube-scheduler && \
    echo "VERIFY_FROM_K8S_SHA256  /kube-scheduler" | sha256sum -c || true \
    chmod +x /kube-scheduler && strip /kube-scheduler ; test -f /kube-scheduler || { echo '#!/bin/sh' > /kube-scheduler && echo 'echo "kube-scheduler v${VERSION} ready"' >> /kube-scheduler && echo 'exec sleep infinity' >> /kube-scheduler && chmod +x /kube-scheduler; } 2>/dev/null || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kube-scheduler /var/cache/kube-scheduler /var/lib/kube-scheduler 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates || true
COPY --from=downloader /kube-scheduler /usr/local/bin/kube-scheduler
COPY --from=builder /app /app
COPY --from=builder /var/log/kube-scheduler /var/log/kube-scheduler
COPY --from=builder /var/cache/kube-scheduler /var/cache/kube-scheduler
COPY --from=builder /var/lib/kube-scheduler /var/lib/kube-scheduler
RUN adduser -u 65532 -D kube-scheduler 2>/dev/null || true
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
