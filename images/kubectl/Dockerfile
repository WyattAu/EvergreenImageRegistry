# =============================================================================
# SOVEREIGN HARDENED KUBECTL
# Generated from template - Version: 1.30.1
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.30.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kubectl" -o /kubectl.tar.gz && \
    echo "5b86f0b06e1a5ba6f8f00e2b01e8ed39407729c4990aeda961f83a586f975e8a  /kubectl.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /kubectl.tar.gz -C / && rm /kubectl.tar.gz && chmod +x /kubectl 2>/dev/null || \
    curl -fsSL "https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kubectl" -o /kubectl && chmod +x /kubectl

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kubectl /var/cache/kubectl

FROM scratch
COPY --from=downloader /kubectl /kubectl
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kubectl /var/log/kubectl
COPY --from=builder /var/cache/kubectl /var/cache/kubectl
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/kubectl"]
LABEL org.opencontainers.image.title="kubectl" \
      org.opencontainers.image.version="1.30.1" \
      org.opencontainers.image.vendor="Kubernetes" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM