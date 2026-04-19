# =============================================================================
# SOVEREIGN HARDENED VAULT-SECRETS
# Generated from template - Version: 0.4.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.4.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/hashicorp/vault-secrets-operator/releases/download/v0.4.0/vault-secrets-operator-0.4.0-linux-amd64.tar.gz" -o /vault-secrets-operator.tar.gz && \
    tar -xzf /vault-secrets-operator.tar.gz -C / && rm /vault-secrets-operator.tar.gz && chmod +x /vault-secrets-operator 2>/dev/null || \
    curl -fsSL "https://github.com/hashicorp/vault-secrets-operator/releases/download/v0.4.0/vault-secrets-operator-0.4.0-linux-amd64.tar.gz" -o /vault-secrets-operator && chmod +x /vault-secrets-operator

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/vault-secrets-operator /var/cache/vault-secrets-operator

FROM scratch
COPY --from=downloader /vault-secrets-operator /vault-secrets-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vault-secrets-operator /var/log/vault-secrets-operator
COPY --from=builder /var/cache/vault-secrets-operator /var/cache/vault-secrets-operator
USER 65534:65534
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/vault", "version"]
ENTRYPOINT ["/vault-secrets-operator"]
LABEL org.opencontainers.image.title="vault-secrets" \
      org.opencontainers.image.version="0.4.0" \
      org.opencontainers.image.vendor="HashiCorp" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
