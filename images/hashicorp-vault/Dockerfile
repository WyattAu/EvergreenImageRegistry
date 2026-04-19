# =============================================================================
# SOVEREIGN HARDENED HASHICORP-VAULT
# Generated from template - Version: 1.18.1
# =============================================================================

ARG VERSION=1.18.1
ARG BUILD_DATE

FROM alpine:3.21 AS downloader
RUN apk add --no-cache curl ca-certificates tar gzip
RUN curl -fsSL "https://releases.hashicorp.com/vault/1.18.1/vault_1.18.1_linux_amd64.zip" -o /vault.tar.gz && \
    tar -xzf /vault.tar.gz -C / && rm /vault.tar.gz && chmod +x /vault

FROM scratch
COPY --from=downloader /vault /vault
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN chown root:root /vault && chmod +x /vault
RUN mkdir -p /app /var/log/vault /var/cache/vault && chown 65534:65534 /app /var/log/vault /var/cache/vault
USER 65534:65534
WORKDIR /app
EXPOSE 8200 8201
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost:8200//v1/sys/health || exit 1
ENTRYPOINT ["/vault"]
LABEL org.opencontainers.image.title="hashicorp-vault" \
      org.opencontainers.image.version="1.18.1" \
      org.opencontainers.image.vendor="HashiCorp" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.static="true"
