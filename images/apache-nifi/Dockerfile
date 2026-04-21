# =============================================================================
# SOVEREIGN HARDENED APACHE-NIFI
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
RUN curl -fsSL "https://archive.apache.org/dist/nifi/${VERSION}/nifi-${VERSION}-bin.zip" \
    -o /nifi.zip \
    && echo "9feb9a6b8b002f17f0cfe4dc7f9f77bebc8608bdec6ec47bfddffa06934db79f  /nifi.zip" | sha256sum -c - \
    && unzip -q /nifi.zip -d /opt \
    && rm /nifi.zip

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin nifi 2>/dev/null || true
RUN mkdir -p /var/lib/nifi /var/log/nifi /var/cache/nifi
COPY --from=builder /opt/nifi-${VERSION} /opt/nifi
RUN chown -R nifi:nifi /opt/nifi /var/lib/nifi /var/log/nifi /var/cache/nifi
USER 65534:65534
WORKDIR /opt/nifi
EXPOSE 8443
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["curl", "-fk", "https://localhost:8443/nifi-api/system-diagnostics"]
ENTRYPOINT ["/opt/nifi/bin/nifi.sh", "run"]
LABEL org.opencontainers.image.title="apache-nifi" \
      org.opencontainers.image.version="1.26.0" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.description="Sovereign hardened Apache NiFi - data integration and flow management platform" \
      sovereign.image.tier="1" \
      sovereign.image.category="data-flow" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
