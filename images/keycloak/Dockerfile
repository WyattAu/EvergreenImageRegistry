# =============================================================================
# SOVEREIGN HARDENED KEYCLOAK
# Generated from template - Version: 26.0.5
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=26.0.5
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:20240415 AS downloader
RUN apk add --no-cache openjdk-17 curl ca-certificates
RUN curl -fsSL "https://github.com/keycloak/keycloak/releases/download/26.0.5/keycloak-26.0.5.tar.gz" -o /keycloak.tar.gz && tar -xzf /keycloak.tar.gz -C / && mv /keycloak-26.0.5 /keycloak && rm /keycloak.tar.gz && \
    echo "f3290d506f895d9e474e04d8d108290f12ee04b51e044289295c79d696838974  /keycloak.tar.gz" | sha256sum -c - && \

FROM cgr.dev/chainguard/wolfi-base:20240415
RUN addgroup -g 65534 keycloak || true
RUN adduser -D -u 65534 -G keycloak keycloak || true
RUN mkdir -p /app /var/log/keycloak /var/cache/keycloak
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
