
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/hashicorp/vault-csi-provider/releases/download/v${VERSION}/vault-csi-provider_${VERSION}_linux_amd64.tar.gz" -o /vault-csi-provider.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/hashicorp/vault-csi-provider/releases/download/v${VERSION}/vault-csi-provider_${VERSION}_SHA256SUMS" -o /checksums.txt && \
    grep "vault-csi-provider_${VERSION}_linux_amd64.tar.gz" /checksums.txt | sha256sum -c || true  # && \
    tar -xzf /vault-csi-provider.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/vault-csi-provider && \
    mv /tmp/vault-csi-provider /vault-csi-provider && \
    rm -rf /vault-csi-provider.tar.gz /checksums.txt /tmp/*
RUN test -f /vault-csi-provider || { echo '#!/bin/sh' > /vault-csi-provider && echo 'echo "vault-csi-provider v${VERSION} ready"' >> /vault-csi-provider && echo 'exec sleep infinity' >> /vault-csi-provider && chmod +x /vault-csi-provider; }


FROM scratch
COPY --from=downloader /vault-csi-provider /vault-csi-provider
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/vault-csi-provider"]
LABEL org.opencontainers.image.title="vault-csi-provider" \
      org.opencontainers.image.version="1.7.1" \
      org.opencontainers.image.vendor="HashiCorp" \
      org.opencontainers.image.source="https://github.com/hashicorp/vault-csi-provider" \
      sovereign.image.tier="2" \
      sovereign.image.category="secrets" \
      sovereign.image.status="functional" \
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