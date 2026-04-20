# =============================================================================
# SOVEREIGN HARDENED VAULTWARDEN
# Generated from template - Version: 2024.4.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2024.4.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/dani-garcia/vaultwarden/releases/download/${VERSION}/vaultwarden-${VERSION}-linux-amd64.tar.gz" -o /tmp/vaultwarden.tar.gz && \
    tar -xzf /tmp/vaultwarden.tar.gz -C /usr/local/bin && rm /tmp/vaultwarden.tar.gz && \
    chmod +x /usr/local/bin/vaultwarden
RUN useradd -m -u 65534 -g '' vaultwarden 2>/dev/null || true
RUN mkdir -p /app /var/log/vaultwarden /var/cache/vaultwarden && chown -R vaultwarden:vaultwarden /app /var/log/vaultwarden /var/cache/vaultwarden 2>/dev/null || true
USER vaultwarden
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD vaultwarden --version
ENTRYPOINT ["vaultwarden"]
LABEL org.opencontainers.image.title="vaultwarden" \
      org.opencontainers.image.version="2024.4.1" \
      org.opencontainers.image.vendor="Vaultwarden" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
