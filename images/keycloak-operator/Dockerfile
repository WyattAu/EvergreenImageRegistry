# =============================================================================
# SOVEREIGN HARDENED KEYCLOAK OPERATOR
# Kubernetes operator for Keycloak - Go static binary
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=24.0.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/keycloak/keycloak-operator/releases/download/${VERSION}/keycloak-operator_${VERSION}_linux_amd64.tar.gz" -o /keycloak-operator.tar.gz && \
    curl -fsSL "https://github.com/keycloak/keycloak-operator/releases/download/${VERSION}/checksums.txt" -o /checksums.txt && \
    grep "keycloak-operator_${VERSION}_linux_amd64.tar.gz" /checksums.txt | sha256sum -c - && \
    tar -xzf /keycloak-operator.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/keycloak-operator && \
    mv /tmp/keycloak-operator /keycloak-operator && \
    rm -rf /keycloak-operator.tar.gz /checksums.txt /tmp/*

FROM scratch
COPY --from=downloader /keycloak-operator /keycloak-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/keycloak-operator"]
LABEL org.opencontainers.image.title="keycloak-operator" \
      org.opencontainers.image.version="24.0.2" \
      org.opencontainers.image.vendor="Keycloak" \
      org.opencontainers.image.source="https://github.com/keycloak/keycloak-operator" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM