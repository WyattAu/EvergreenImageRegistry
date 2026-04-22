# =============================================================================
# SOVEREIGN HARDENED CERTIFICATES (CFSSL)
# Cloudflare TLS toolkit - Go static binary
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.6.5
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/cloudflare/cfssl/releases/download/v${VERSION}/cfssl_1.6.5_linux_amd64" -o /cfssl && \
    curl -fsSL "https://github.com/cloudflare/cfssl/releases/download/v${VERSION}/cfssljson_1.6.5_linux_amd64" -o /cfssljson && \
    curl -fsSL "https://github.com/cloudflare/cfssl/releases/download/v${VERSION}/mkbundle_1.6.5_linux_amd64" -o /mkbundle && \
    chmod +x /cfssl /cfssljson /mkbundle && \
    strip --strip-all /cfssl /cfssljson /mkbundle

FROM scratch
COPY --from=downloader /cfssl /cfssl
COPY --from=downloader /cfssljson /cfssljson
COPY --from=downloader /mkbundle /mkbundle
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/cfssl", "version"]
ENTRYPOINT ["/cfssl"]
LABEL org.opencontainers.image.title="certificates" \
      org.opencontainers.image.version="1.6.5" \
      org.opencontainers.image.vendor="Cloudflare" \
      org.opencontainers.image.source="https://github.com/cloudflare/cfssl" \
      sovereign.image.tier="2" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
