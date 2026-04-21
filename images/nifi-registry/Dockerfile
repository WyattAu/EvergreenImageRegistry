# =============================================================================
# SOVEREIGN HARDENED NIFI-REGISTRY
# Generated from template - Version: 1.26.0
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.26.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://archive.apache.org/dist/nifi/${VERSION}/nifi-registry-${VERSION}-bin.zip" \
    -o /nifi-registry.zip \
    && echo "af7b39f6bceacfd4e2e4f8805e9da9f7faea3ea9a7b031748f51c6cf72fd7021  /nifi-registry.zip" | sha256sum -c - \
    && unzip -q /nifi-registry.zip -d /opt \
    && rm /nifi-registry.zip

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin nifi 2>/dev/null || true
RUN mkdir -p /var/lib/nifi-registry /var/log/nifi-registry /var/cache/nifi-registry
COPY --from=builder /opt/nifi-registry-${VERSION} /opt/nifi-registry
RUN chown -R nifi:nifi /opt/nifi-registry /var/lib/nifi-registry /var/log/nifi-registry /var/cache/nifi-registry
USER 65534:65534
WORKDIR /opt/nifi-registry
EXPOSE 18080
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["curl", "-f", "http://localhost:18080/nifi-registry/api/about"]
ENTRYPOINT ["/opt/nifi-registry/bin/nifi-registry.sh", "run"]
LABEL org.opencontainers.image.title="nifi-registry" \
      org.opencontainers.image.version="1.26.0" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.description="Sovereign hardened NiFi Registry - versioned flow management for Apache NiFi" \
      sovereign.image.tier="1" \
      sovereign.image.category="data-flow" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
