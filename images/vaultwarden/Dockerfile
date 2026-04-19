# =============================================================================
# SOVEREIGN HARDENED VAULTWARDEN
# Generated from template - Version: 2026.4.1
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=2026.4.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends vaultwarden ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' vaultwarden 2>/dev/null || true
RUN mkdir -p /app /var/log/vaultwarden /var/cache/vaultwarden && chown -R vaultwarden:vaultwarden /app /var/log/vaultwarden /var/cache/vaultwarden 2>/dev/null || true
USER vaultwarden:vaultwarden
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /alive
ENTRYPOINT ["vaultwarden"]
LABEL org.opencontainers.image.title="vaultwarden" \
      org.opencontainers.image.version="2026.4.1" \
      org.opencontainers.image.vendor="Vaultwarden" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
