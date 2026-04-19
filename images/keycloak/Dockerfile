# =============================================================================
# SOVEREIGN HARDENED KEYCLOAK
# Generated from template - Version: 26.0.5
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=26.0.5
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends openjdk17 curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' keycloak 2>/dev/null || true
RUN mkdir -p /app /var/log/keycloak /var/cache/keycloak && chown -R keycloak:keycloak /app /var/log/keycloak /var/cache/keycloak 2>/dev/null || true
USER keycloak
WORKDIR /app
EXPOSE 8080 8443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD keycloak curl -s localhost:8080/health/ready
ENTRYPOINT ["keycloak"]
LABEL org.opencontainers.image.title="keycloak" \
      org.opencontainers.image.version="26.0.5" \
      org.opencontainers.image.vendor="Keycloak" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
