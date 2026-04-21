# =============================================================================
# SOVEREIGN HARDENED AGE
# Simple, modern file encryption tool
# Constraint: scratch - static Go binary, no runtime deps
# =============================================================================

ARG VERSION=1.1.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/FiloSottile/age/releases/download/v${VERSION}/age-v${VERSION}-linux-amd64.tar.gz" -o /age.tar.gz && \
    tar -xzf /age.tar.gz -C / && rm /age.tar.gz && chmod +x /age/age /age/age-keygen

FROM scratch
COPY --from=downloader /age/age /usr/local/bin/age
COPY --from=downloader /age/age-keygen /usr/local/bin/age-keygen
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /tmp
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/usr/local/bin/age", "--version"]
ENTRYPOINT ["/usr/local/bin/age"]
LABEL org.opencontainers.image.title="age" \
      org.opencontainers.image.version="1.1.1" \
      org.opencontainers.image.vendor="FiloSottile" \
      org.opencontainers.image.source="https://github.com/FiloSottile/age" \
      org.opencontainers.image.description="Simple, modern file encryption tool" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="1000ms"
