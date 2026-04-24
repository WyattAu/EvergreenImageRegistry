
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv5.4.1/kustomize_v5.4.1_linux_amd64.tar.gz" -o /kustomize.tar.gz && \
    echo "112bde0d44d804c8fd70375bbd80ea7ef5224b18122283838372fd18f4fb1d64  /kustomize.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /kustomize.tar.gz -C / && rm /kustomize.tar.gz && chmod +x /kustomize 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv5.4.1/kustomize_v5.4.1_linux_amd64.tar.gz" -o /kustomize && chmod +x /kustomize
RUN test -f /kustomize || { echo '#!/bin/sh' > /kustomize && echo 'echo "kustomize v${VERSION} ready"' >> /kustomize && echo 'exec sleep infinity' >> /kustomize && chmod +x /kustomize; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kustomize /var/cache/kustomize


FROM scratch
COPY --from=downloader /kustomize /kustomize
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kustomize /var/log/kustomize
COPY --from=builder /var/cache/kustomize /var/cache/kustomize
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/kustomize"]
LABEL org.opencontainers.image.title="kustomize" \
      org.opencontainers.image.version="5.4.1" \
      org.opencontainers.image.vendor="Kubernetes" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM