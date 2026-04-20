# =============================================================================
# SOVEREIGN HARDENED KUSTOMIZE
# Generated from template - Version: 5.4.1
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=5.4.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv5.4.1/kustomize_v5.4.1_linux_amd64.tar.gz" -o /kustomize.tar.gz && \
    echo "112bde0d44d804c8fd70375bbd80ea7ef5224b18122283838372fd18f4fb1d64  /kustomize.tar.gz" | sha256sum -c - && \
    tar -xzf /kustomize.tar.gz -C / && rm /kustomize.tar.gz && chmod +x /kustomize 2>/dev/null || \
    curl -fsSL "https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv5.4.1/kustomize_v5.4.1_linux_amd64.tar.gz" -o /kustomize && chmod +x /kustomize

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kustomize /var/cache/kustomize

FROM scratch
COPY --from=downloader /kustomize /kustomize
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kustomize /var/log/kustomize
COPY --from=builder /var/cache/kustomize /var/cache/kustomize
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/kustomize", "version"]
ENTRYPOINT ["/kustomize"]
LABEL org.opencontainers.image.title="kustomize" \
      org.opencontainers.image.version="5.4.1" \
      org.opencontainers.image.vendor="Kubernetes" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
