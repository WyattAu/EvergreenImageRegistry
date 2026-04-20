# =============================================================================
# SOVEREIGN HARDENED HELM
# Generated from template - Version: 3.15.1
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.15.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://get.helm.sh/helm-v3.15.1-linux-amd64.tar.gz" -o /helm.tar.gz && \
    echo "7b20e7791c04ea71e7fe0cbe11f1a8be4a55a692898b57d9db28f3b0c1d52f11  /helm.tar.gz" | sha256sum -c - && \
    tar -xzf /helm.tar.gz -C / && rm /helm.tar.gz && chmod +x /helm 2>/dev/null || \
    curl -fsSL "https://get.helm.sh/helm-v3.15.1-linux-amd64.tar.gz" -o /helm && chmod +x /helm

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/helm /var/cache/helm

FROM scratch
COPY --from=downloader /helm /helm
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/helm /var/log/helm
COPY --from=builder /var/cache/helm /var/cache/helm
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/helm", "version"]
ENTRYPOINT ["/helm"]
LABEL org.opencontainers.image.title="helm" \
      org.opencontainers.image.version="3.15.1" \
      org.opencontainers.image.vendor="Helm" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
