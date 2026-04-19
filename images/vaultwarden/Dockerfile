# =============================================================================
# SOVEREIGN HARDENED VAULTWARDEN
# Generated from template - Version: 2026.4.1
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=2026.4.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:2026.4.1
RUN apk add --no-cache vaultwarden ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 vaultwarden 2>/dev/null || true
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
      sovereign.constraint.wolfi="true"
