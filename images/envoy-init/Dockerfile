# =============================================================================
# SOVEREIGN HARDENED ENVOY-INIT
# Generated from template - Version: 1.31.0
# Constraint: distroless - minimal base with glibc, CVE-free
# Priority: scratch > distroless (best) > wolfi > debian-slim
# =============================================================================

ARG VERSION=1.31.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL -k "https://github.com/envoyproxy/envoy/releases/download/v${VERSION}/envoy-${VERSION}-linux-x86_64" -o /envoy && chmod +x /envoy

FROM gcr.io/distroless/cc-debian12@sha256:af49995f9f06255ca7d955735e5484a92018f4cfe95910952d9aee165cb96940
COPY --from=downloader /envoy /envoy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER nonroot
WORKDIR /app
EXPOSE 15001
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/envoy", "--version"]
ENTRYPOINT ["/envoy"]
LABEL org.opencontainers.image.title="envoy-init" \
      org.opencontainers.image.version="1.31.0" \
      org.opencontainers.image.vendor="Envoy" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distroless="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="0-1" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-rolling" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true"
