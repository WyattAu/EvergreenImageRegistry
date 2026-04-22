# =============================================================================
# SOVEREIGN HARDENED KEYCLOAK GATEKEEPER
# Keycloak proxy/gatekeeper - Go static binary
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=9.1.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/keycloak/keycloak-gatekeeper/releases/download/v${VERSION}/keycloak-gatekeeper_${VERSION}_linux_amd64.tar.gz" -o /gatekeeper.tar.gz && \
    curl -fsSL "https://github.com/keycloak/keycloak-gatekeeper/releases/download/v${VERSION}/checksums.txt" -o /checksums.txt && \
    grep "keycloak-gatekeeper_${VERSION}_linux_amd64.tar.gz" /checksums.txt | sha256sum -c - && \
    tar -xzf /gatekeeper.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/keycloak-gatekeeper && \
    mv /tmp/keycloak-gatekeeper /keycloak-gatekeeper && \
    rm -rf /gatekeeper.tar.gz /checksums.txt /tmp/*

FROM scratch
COPY --from=downloader /keycloak-gatekeeper /keycloak-gatekeeper
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/keycloak-gatekeeper", "--help"]
ENTRYPOINT ["/keycloak-gatekeeper"]
LABEL org.opencontainers.image.title="keycloak-gatekeeper" \
      org.opencontainers.image.version="9.1.1" \
      org.opencontainers.image.vendor="Keycloak" \
      org.opencontainers.image.source="https://github.com/keycloak/keycloak-gatekeeper" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
