# =============================================================================
# SOVEREIGN HARDENED HASHICORP VAULT ENTERPRISE
# HashiCorp Vault Enterprise - Placeholder
# NOTE: Vault Enterprise requires a license and is not available as a
# public binary download. This image provides a functional placeholder
# that mirrors the OSS vault image structure.
# =============================================================================

ARG BUILD_DATE

FROM debian:bookworm-slim AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        unzip && \
    curl -fsSL "https://releases.hashicorp.com/vault/1.18.5/vault_1.18.5_linux_amd64.zip" -o /vault.zip && \
    curl -fsSL "https://releases.hashicorp.com/vault/1.18.5/vault_1.18.5_SHA256SUMS" -o /checksums.txt && \
    curl -fsSL "https://releases.hashicorp.com/vault/1.18.5/vault_1.18.5_SHA256SUMS.sig" -o /checksums.sig && \
    grep "vault_1.18.5_linux_amd64.zip" /checksums.txt | sha256sum -c - && \
    unzip /vault.zip -d /usr/local/bin/ && \
    rm -f /vault.zip /checksums.txt /checksums.sig && \
    strip --strip-all /usr/local/bin/vault && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app && chown 65534:65534 /app
USER 65534:65534
WORKDIR /app
EXPOSE 8200
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/vault", "status"]
ENTRYPOINT ["/usr/local/bin/vault"]
CMD ["server", "-dev"]
LABEL org.opencontainers.image.title="hashicorp-vault-enterprise" \
      org.opencontainers.image.description="HashiCorp Vault Enterprise placeholder (uses OSS binary; Enterprise requires license)" \
      org.opencontainers.image.version="1.18.5" \
      org.opencontainers.image.vendor="HashiCorp" \
      org.opencontainers.image.source="https://www.hashicorp.com/products/vault/enterprise" \
      sovereign.image.tier="2" \
      sovereign.image.category="secrets" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
