# =============================================================================
# SOVEREIGN HARDENED ENVOY-SIDECAR
# Generated from template - Version: 1.31.0
# Constraint: distroless - minimal base with glibc, CVE-free
# Priority: scratch > distroless (best) > wolfi > debian-slim
# =============================================================================

ARG VERSION=1.31.0
ARG BUILD_DATE

FROM gcr.io/distroless/cc-debian12@sha256:af49995f9f06255ca7d955735e5484a92018f4cfe95910952d9aee165cb96940 AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/envoyproxy/envoy/releases/download/v1.31.0/envoy-1.31.0.tar.gz" -o /envoy.tar.gz && \
    tar -xzf /envoy.tar.gz -C / && rm /envoy.tar.gz && chmod +x /envoy 2>/dev/null || \
    curl -fsSL "https://github.com/envoyproxy/envoy/releases/download/v1.31.0/envoy-1.31.0.tar.gz" -o /envoy && chmod +x /envoy

FROM gcr.io/distroless/cc-debian12@sha256:af49995f9f06255ca7d955735e5484a92018f4cfe95910952d9aee165cb96940
COPY --from=downloader /envoy /envoy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN mkdir -p /app /var/log/envoy /var/cache/envoy
USER nonroot
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/envoy", "--version"]
ENTRYPOINT ["/envoy"]
LABEL org.opencontainers.image.title="envoy-sidecar" \
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
