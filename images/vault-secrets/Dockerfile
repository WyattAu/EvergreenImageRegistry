# =============================================================================
# SOVEREIGN HARDENED VAULT SECRETS OPERATOR
# HashiCorp Vault Secrets Operator for Kubernetes
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.4.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/hashicorp/vault-secrets-operator/releases/download/v${VERSION}/vault-secrets-operator_${VERSION}_linux_amd64.zip" -o /vault-secrets.zip && \
    curl -fsSL "https://github.com/hashicorp/vault-secrets-operator/releases/download/v${VERSION}/vault-secrets-operator_${VERSION}_SHA256SUMS" -o /checksums.txt && \
    grep "vault-secrets-operator_${VERSION}_linux_amd64.zip" /checksums.txt | sha256sum -c - && \
    unzip -o /vault-secrets.zip -d /tmp/ && \
    strip --strip-all /tmp/vault-secrets-operator && \
    mv /tmp/vault-secrets-operator /vault-secrets-operator && \
    rm -rf /vault-secrets.zip /checksums.txt /tmp/*

FROM scratch
COPY --from=downloader /vault-secrets-operator /vault-secrets-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 8080 8443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/vault-secrets-operator", "--help"]
ENTRYPOINT ["/vault-secrets-operator"]
LABEL org.opencontainers.image.title="vault-secrets" \
      org.opencontainers.image.version="1.4.0" \
      org.opencontainers.image.vendor="HashiCorp" \
      org.opencontainers.image.source="https://github.com/hashicorp/vault-secrets-operator" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
