# =============================================================================
# SOVEREIGN HARDENED VAULT
# Generated from template - Version: 1.18.1
# Constraint: distroless/static - no shell, no package manager
# =============================================================================

ARG VERSION=1.18.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://releases.hashicorp.com/vault/1.18.1/vault_1.18.1_linux_amd64.zip" -o /vault.tar.gz && \
    tar -xzf /vault.tar.gz -C / && rm /vault.tar.gz && chmod +x /vault

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/vault /var/cache/vault

FROM gcr.io/distroless/static:nonroot
COPY --from=downloader /vault /vault
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vault /var/log/vault
COPY --from=builder /var/cache/vault /var/cache/vault
USER 65534:65534
WORKDIR /app
EXPOSE 8200 8201
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD vault --version 2>/dev/null || exit 1
ENTRYPOINT ["/vault"]
LABEL org.opencontainers.image.title="vault" \
      org.opencontainers.image.version="1.18.1" \
      org.opencontainers.image.vendor="HashiCorp" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distroless="true"
