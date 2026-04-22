# =============================================================================
# SOVEREIGN HARDENED VAULTWARDEN (no-Alpine variant)
# Bitwarden-compatible password manager - Rust static binary on scratch
# NOTE: Alpine is banned per project constraints; using scratch instead
# =============================================================================

ARG VERSION=1.35.7
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/dani-garcia/vaultwarden/releases/download/${VERSION}/vaultwarden-linux-amd64" -o /vaultwarden && \
    chmod +x /vaultwarden && \
    strip --strip-all /vaultwarden

FROM scratch
COPY --from=downloader /vaultwarden /vaultwarden
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/vaultwarden", "--help"]
ENTRYPOINT ["/vaultwarden"]
LABEL org.opencontainers.image.title="vaultwarden-alpine" \
      org.opencontainers.image.description="Vaultwarden on scratch (Alpine banned per project policy)" \
      org.opencontainers.image.version="1.35.7" \
      org.opencontainers.image.vendor="dani-garcia" \
      org.opencontainers.image.source="https://github.com/dani-garcia/vaultwarden" \
      sovereign.image.tier="2" \
      sovereign.image.category="secrets" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
