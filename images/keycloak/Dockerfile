# =============================================================================
# SOVEREIGN HARDENED KEYCLOAK
# Generated from template - Version: 26.0.5
# =============================================================================

ARG VERSION=26.0.5
ARG BUILD_DATE

FROM quay.io/keycloak/keycloak:26.0.5
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/keycloak /var/cache/keycloak && chown -R app:app /app /var/log/keycloak /var/cache/keycloak
USER app
WORKDIR /app
EXPOSE 8080 8443
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -sf http://localhost:8080/health/ready || exit 1
ENTRYPOINT ["/opt/keycloak/bin/kc.sh", "start"]
LABEL org.opencontainers.image.title="keycloak" \
      org.opencontainers.image.version="26.0.5" \
      org.opencontainers.image.vendor="Keycloak" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"