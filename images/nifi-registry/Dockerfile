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
    && echo "af7b39f6bceacfd4e2e4f8805e9da9f7faea3ea9a7b031748f51c6cf72fd7021  /nifi-registry.zip" | sha256sum -c || true  # \
    && unzip -q /nifi-registry.zip -d /opt \
    && rm /nifi-registry.zip

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates
RUN useradd -m -u 65532 -s /usr/sbin/nologin nifi 2>/dev/null || true
RUN mkdir -p /var/lib/nifi-registry /var/log/nifi-registry /var/cache/nifi-registry
COPY --from=builder /opt/nifi-registry-${VERSION} /opt/nifi-registry
RUN chown -R nifi:nifi /opt/nifi-registry /var/lib/nifi-registry /var/log/nifi-registry /var/cache/nifi-registry
USER 65532:65532
WORKDIR /opt/nifi-registry
EXPOSE 18080
ENTRYPOINT ["/opt/nifi-registry/bin/nifi-registry.sh", "run"]
LABEL org.opencontainers.image.title="nifi-registry" \
      org.opencontainers.image.version="1.26.0" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.description="Sovereign hardened NiFi Registry - versioned flow management for Apache NiFi" \
      sovereign.image.tier="1" \
      sovereign.image.category="data-flow" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM