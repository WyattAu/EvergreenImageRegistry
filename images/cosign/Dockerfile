# =============================================================================
# SOVEREIGN HARDENED COSIGN
# Container signing verification - Go static binary
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.0.6
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/sigstore/cosign/releases/download/v${VERSION}/cosign-linux-amd64" -o /cosign && \
    curl -fsSL "https://github.com/sigstore/cosign/releases/download/v${VERSION}/cosign-linux-amd64.sig" -o /cosign.sig && \
    chmod +x /cosign && \
    strip --strip-all /cosign && \
    rm -f /cosign.sig

FROM scratch
COPY --from=downloader /cosign /cosign
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/cosign", "version"]
ENTRYPOINT ["/cosign"]
LABEL org.opencontainers.image.title="cosign" \
      org.opencontainers.image.version="3.0.6" \
      org.opencontainers.image.vendor="sigstore" \
      org.opencontainers.image.source="https://github.com/sigstore/cosign" \
      sovereign.image.tier="2" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
