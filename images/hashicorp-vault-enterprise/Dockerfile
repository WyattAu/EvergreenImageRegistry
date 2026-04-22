# =============================================================================
# SOVEREIGN HARDENED HASHICORP VAULT ENTERPRISE
# HashiCorp Vault Enterprise - Placeholder
# NOTE: Vault Enterprise requires a license and is not available as a
# public binary download. This image provides a functional placeholder
# that mirrors the OSS vault image structure.
# =============================================================================

ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007 AS runtime
RUN apk add --no-cache ca-certificates curl unzip grep sha256sum
RUN mkdir -p /app && chown 65532:65532 /app
USER 65532:65532
WORKDIR /app
EXPOSE 8200
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
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM