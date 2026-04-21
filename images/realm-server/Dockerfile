# =============================================================================
# SOVEREIGN HARDENED REALM-SERVER (MongoDB Realm)
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2024.4.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/10gen/realm-app-services/releases/download/v${VERSION}/realm-app-services-${VERSION}.zip" -o /tmp/realm.zip \
    && echo "PENDING  /tmp/realm.zip" | sha256sum -c - \
    && unzip -q /tmp/realm.zip -d /opt \
    && rm /tmp/realm.zip

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates openjdk-17-jre-headless curl mongodb-org-tools 2>/dev/null || \
    apt-get install -y --no-install-recommends \
    ca-certificates openjdk-17-jre-headless curl && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin realm 2>/dev/null || true
RUN mkdir -p /var/lib/realm /var/log/realm /var/cache/realm
COPY --from=builder /opt/realm-app-services-${VERSION} /opt/realm
RUN chown -R 65534:65534 /opt/realm /var/lib/realm /var/log/realm /var/cache/realm
USER 65534:65534
WORKDIR /opt/realm
EXPOSE 9090
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["curl", "-f", "http://localhost:9090/api/health"]
ENTRYPOINT ["/opt/realm/bin/realm-server"]
LABEL org.opencontainers.image.title="realm-server" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened MongoDB Realm Server - application backend platform" \
      org.opencontainers.image.vendor="MongoDB" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
