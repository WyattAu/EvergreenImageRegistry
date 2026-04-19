# =============================================================================
# SOVEREIGN HARDENED KEYCLOAK
# Generated from template - Version: 26.0.5
# =============================================================================

ARG VERSION=26.0.5
ARG BUILD_DATE

FROM quay.io/keycloak/keycloak:26.0.5-minimal
RUN apk add --no-cache keycloak ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id keycloak 2>/dev/null || adduser -D -u 65534 keycloak
RUN mkdir -p /app /var/log/keycloak /var/cache/keycloak && chown -R keycloak:keycloak /app /var/log/keycloak /var/cache/keycloak
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
      sovereign.constraint.nonroot="true"
