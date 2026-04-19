# =============================================================================
# SOVEREIGN HARDENED KEYCLOAK
# Generated from template - Version: 26.0.5
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=26.0.5
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest AS downloader
RUN apk add --no-cache openjdk-17 curl ca-certificates
RUN curl -fsSL "https://github.com/keycloak/keycloak/releases/download/${VERSION}/keycloak-${VERSION}.tar.gz" -o /keycloak.tar.gz && tar -xzf /keycloak.tar.gz -C / && rm /keycloak.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest
RUN adduser -D -u 65534 keycloak
RUN mkdir -p /app /var/log/keycloak /var/cache/keycloak
COPY --from=downloader /keycloak /app/keycloak
USER keycloak
WORKDIR /app
EXPOSE 8080 8443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /app/keycloak/bin/kc.sh start-dev --health-enabled=true
ENTRYPOINT ["/app/keycloak/bin/kc.sh"]
LABEL org.opencontainers.image.title="keycloak" \
      org.opencontainers.image.version="26.0.5" \
      org.opencontainers.image.vendor="Keycloak" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
