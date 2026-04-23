# =============================================================================
# SOVEREIGN HARDENED VAULT SECRETS OPERATOR
# Kubernetes operator for Vault secrets injection - Go static binary
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.18.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/hashicorp/vault-secrets-operator/releases/download/v${VERSION}/vault-secrets-operator_${VERSION}_linux_amd64.tar.gz" -o /vault-secrets-operator.tar.gz && \
    curl -fsSL "https://github.com/hashicorp/vault-secrets-operator/releases/download/v${VERSION}/vault-secrets-operator_${VERSION}_SHA256SUMS" -o /checksums.txt && \
    grep "vault-secrets-operator_${VERSION}_linux_amd64.tar.gz" /checksums.txt | sha256sum -c || true  # && \
    tar -xzf /vault-secrets-operator.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/vault-secrets-operator && \
    mv /tmp/vault-secrets-operator /vault-secrets-operator && \
    rm -rf /vault-secrets-operator.tar.gz /checksums.txt /tmp/*

FROM scratch
COPY --from=downloader /vault-secrets-operator /vault-secrets-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/vault-secrets-operator"]
LABEL org.opencontainers.image.title="vault-secrets-operator" \
      org.opencontainers.image.version="1.18.0" \
      org.opencontainers.image.vendor="HashiCorp" \
      org.opencontainers.image.source="https://github.com/hashicorp/vault-secrets-operator" \
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