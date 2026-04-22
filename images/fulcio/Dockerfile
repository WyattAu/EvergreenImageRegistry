# =============================================================================
# SOVEREIGN HARDENED FULCIO
# Sigstore certificate authority - Go static binary
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.8.5
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/sigstore/fulcio/releases/download/v${VERSION}/fulcio-linux-amd64" -o /fulcio && \
    curl -fsSL "https://github.com/sigstore/fulcio/releases/download/v${VERSION}/fulcio-linux-amd64.sig" -o /fulcio.sig && \
    chmod +x /fulcio && \
    strip --strip-all /fulcio && \
    rm -f /fulcio.sig

FROM scratch
COPY --from=downloader /fulcio /fulcio
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 5555
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/fulcio", "version"]
ENTRYPOINT ["/fulcio"]
LABEL org.opencontainers.image.title="fulcio" \
      org.opencontainers.image.version="1.8.5" \
      org.opencontainers.image.vendor="sigstore" \
      org.opencontainers.image.source="https://github.com/sigstore/fulcio" \
      sovereign.image.tier="2" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
