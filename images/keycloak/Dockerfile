# =============================================================================
# SOVEREIGN HARDENED KEYCLOAK
# Open-source identity and access management - Java app (Quarkus runtime)
# Constraint: debian-slim + JRE - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=26.6.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/keycloak/keycloak/releases/download/${VERSION}/keycloak-${VERSION}.tar.gz" -o /keycloak.tar.gz && \
    curl -fsSL "https://github.com/keycloak/keycloak/releases/download/${VERSION}/keycloak-${VERSION}.tar.gz.sha1" -o /checksums.sha1 && \
    grep "keycloak-${VERSION}.tar.gz" /checksums.sha1 | sha1sum -c - && \
    tar -xzf /keycloak.tar.gz -C /opt/ && \
    rm -rf /keycloak.tar.gz /checksums.sha1

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache ca-certificates
COPY --from=downloader /opt/keycloak-${VERSION} /opt/keycloak
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/keycloak
USER 65532:65532
WORKDIR /app
ENV KEYCLOAK_HOME=/opt/keycloak
EXPOSE 8080 8443
ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
CMD ["start-dev"]
LABEL org.opencontainers.image.title="keycloak" \
      org.opencontainers.image.version="26.6.1" \
      org.opencontainers.image.vendor="Keycloak" \
      org.opencontainers.image.source="https://github.com/keycloak/keycloak" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM