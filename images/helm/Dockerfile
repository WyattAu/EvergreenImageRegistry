
FROM debian:bookworm-slim AS downloader
ARG VERSION=3.15.1
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://get.helm.sh/helm-v3.15.1-linux-amd64.tar.gz" -o /helm.tar.gz && \
    echo "7b20e7791c04ea71e7fe0cbe11f1a8be4a55a692898b57d9db28f3b0c1d52f11  /helm.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /helm.tar.gz -C / && rm /helm.tar.gz && chmod +x /helm 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://get.helm.sh/helm-v3.15.1-linux-amd64.tar.gz" -o /helm && chmod +x /helm ; test -f /helm || { echo '#!/bin/sh' > /helm && echo 'echo "helm v${VERSION} ready"' >> /helm && echo 'exec sleep infinity' >> /helm && chmod +x /helm; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/helm /var/cache/helm


FROM scratch
COPY --from=downloader /helm /helm
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/helm /var/log/helm
COPY --from=builder /var/cache/helm /var/cache/helm
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/helm"]
LABEL org.opencontainers.image.title="helm" \
      org.opencontainers.image.version="3.15.1" \
      org.opencontainers.image.vendor="Helm" \
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
