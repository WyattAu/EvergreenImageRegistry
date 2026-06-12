# =============================================================================
# EVERGREEN HARDENED VAULTWARDEN
# Extract from upstream + wolfi-base (dynamically linked binary)
# Upstream binary needs: libssl, libcrypto, libmariadb, libpq, libc, libz, etc.
# =============================================================================
ARG VERSION=1.36.0
ARG SHIM_VERSION=v1.0.0

FROM vaultwarden/server:${VERSION} AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM --platform=linux/amd64 cgr.dev/chainguard/wolfi-base@sha256:0b5fd36c9f36ecc95bf6dbe049fe0a211410e1ba8a9801db0fbe25c7561d81c1
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN apk add --no-cache \
    openssl \
    mariadb-connector-c \
    postgresql-client \
    zlib \
    zstd \
    krb5-libs \
    openldap \
    ca-certificates

COPY --from=upstream /vaultwarden /vaultwarden
COPY --from=upstream /web-vault /web-vault

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true" ROCKET_PORT=80
WORKDIR /
EXPOSE 80 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/vaultwarden"]
LABEL org.opencontainers.image.title="vaultwarden" \
      org.opencontainers.image.description="Vaultwarden - lightweight Bitwarden-compatible password manager" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="dani-garcia" \
      org.opencontainers.image.source="https://github.com/dani-garcia/vaultwarden"
LABEL evergreen.base.image="wolfi" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.read-only-rootfs="true" \
      evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGTERM
