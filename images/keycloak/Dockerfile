# =============================================================================
# SOVEREIGN HARDENED KEYCLOAK
# Generated from template - Version: 26.0.5
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=26.0.5
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
# hadolint ignore=DL3018
RUN apk add --no-cache openjdk-17 curl ca-certificates
# hadolint ignore=DL4006
RUN curl -fsSL -k "https://github.com/keycloak/keycloak/releases/download/${VERSION}/keycloak-${VERSION}.tar.gz" -o /keycloak.tar.gz && \
    tar -xzf /keycloak.tar.gz -C / && mv /keycloak-${VERSION} /keycloak && rm /keycloak.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest AS runtime
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN addgroup -g 65534 keycloak || true
RUN adduser -D -u 65534 -G keycloak keycloak || true
RUN mkdir -p /app /var/log/keycloak /var/cache/keycloak
# hadolint ignore=DL3023
COPY --from=downloader /keycloak /app/keycloak
USER keycloak
WORKDIR /app
EXPOSE 8080 8443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/app/keycloak/bin/kc.sh", "start-dev", "--health-enabled=true"]
ENTRYPOINT ["/app/keycloak/bin/kc.sh"]
LABEL org.opencontainers.image.title="keycloak" \
      org.opencontainers.image.version="26.0.5" \
      org.opencontainers.image.vendor="Keycloak" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
