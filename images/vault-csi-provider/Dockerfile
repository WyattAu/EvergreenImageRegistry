# =============================================================================
# SOVEREIGN HARDENED VAULT CSI PROVIDER
# HashiCorp Vault CSI secrets provider - Go static binary
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.7.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/hashicorp/vault-csi-provider/releases/download/v${VERSION}/vault-csi-provider_${VERSION}_linux_amd64.tar.gz" -o /vault-csi-provider.tar.gz && \
    curl -fsSL "https://github.com/hashicorp/vault-csi-provider/releases/download/v${VERSION}/vault-csi-provider_${VERSION}_SHA256SUMS" -o /checksums.txt && \
    grep "vault-csi-provider_${VERSION}_linux_amd64.tar.gz" /checksums.txt | sha256sum -c - && \
    tar -xzf /vault-csi-provider.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/vault-csi-provider && \
    mv /tmp/vault-csi-provider /vault-csi-provider && \
    rm -rf /vault-csi-provider.tar.gz /checksums.txt /tmp/*

FROM scratch
COPY --from=downloader /vault-csi-provider /vault-csi-provider
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/vault-csi-provider", "--help"]
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
