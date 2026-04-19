# =============================================================================
# SOVEREIGN HARDENED KEYCLOAK
# Generated from template - Version: 26.0.5
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=26.0.5
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:26.0.5
RUN apk add --no-cache keycloak ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 keycloak 2>/dev/null || true
RUN mkdir -p /app /var/log/keycloak /var/cache/keycloak && chown -R keycloak:keycloak /app /var/log/keycloak /var/cache/keycloak 2>/dev/null || true
USER keycloak:keycloak
WORKDIR /app
EXPOSE 8080 8443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /health/ready
ENTRYPOINT ["keycloak"]
LABEL org.opencontainers.image.title="keycloak" \
      org.opencontainers.image.version="26.0.5" \
      org.opencontainers.image.vendor="Keycloak" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
