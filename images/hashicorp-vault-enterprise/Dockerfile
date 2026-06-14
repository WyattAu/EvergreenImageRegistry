# =============================================================================
# EVERGREEN HARDENED HASHICORP VAULT ENTERPRISE
# HashiCorp Vault Enterprise - Placeholder
# NOTE: Vault Enterprise requires a license and is not available as a
# that mirrors the OSS vault image structure.
# =============================================================================

ARG BUILD_DATE


ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN apk add --no-cache ca-certificates curl unzip RUN mkdir -p /app && chown 65532:65532 /app 2>/dev/null
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8200

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8200"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/usr/local/bin/vault", "--", "server", "-dev"]
LABEL org.opencontainers.image.title="hashicorp-vault-enterprise" \
      org.opencontainers.image.description="hashicorp-vault-enterprise container image" \
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
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
