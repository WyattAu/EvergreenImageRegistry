# =============================================================================
# SOVEREIGN HARDENED COSIGN
# Generated from template - Version: 3.0.6
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.0.6
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/sigstore/cosign/releases/download/v${VERSION}/cosign-linux-amd64" -o /cosign && chmod +x /cosign

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/cosign /var/cache/cosign

FROM scratch
COPY --from=downloader /cosign /cosign
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/cosign /var/log/cosign
COPY --from=builder /var/cache/cosign /var/cache/cosign
USER 65534:65534
WORKDIR /app
EXPOSE 7879
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/cosign", "version"]
ENTRYPOINT ["/cosign"]
LABEL org.opencontainers.image.title="cosign" \
      org.opencontainers.image.version="3.0.6" \
      org.opencontainers.image.vendor="Sigstore" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
