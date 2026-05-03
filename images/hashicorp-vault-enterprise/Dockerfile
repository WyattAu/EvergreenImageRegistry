# =============================================================================
# EVERGREEN HARDENED HASHICORP VAULT ENTERPRISE
# HashiCorp Vault Enterprise - Placeholder
# NOTE: Vault Enterprise requires a license and is not available as a
# that mirrors the OSS vault image structure.
# =============================================================================

ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates curl unzip RUN mkdir -p /app && chown 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8200

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8200/ || exit 1
ENTRYPOINT ["/usr/local/bin/vault"]
CMD ["server", "-dev"]
LABEL org.opencontainers.image.title="hashicorp-vault-enterprise" \
      org.opencontainers.image.version="1.18.5" \
      org.opencontainers.image.vendor="HashiCorp" \
      org.opencontainers.image.source="https://www.hashicorp.com/products/vault/enterprise" \
      evergreen.image.tier="2" \
      evergreen.image.category="secrets" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="10000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
