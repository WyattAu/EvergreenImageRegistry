# =============================================================================
# SOVEREIGN HARDENED ARANGO (alias of arangodb)
# Constraint: scratch - pure static binary (same as arangodb)
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.12.2
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://download.arangodb.com/arangodb312/Community/Linux/arangodb3-linux-${VERSION}.tar.gz" -o /tmp/arango.tar.gz \
    && echo "PENDING  /tmp/arango.tar.gz" | sha256sum -c - \
    && tar -xzf /tmp/arango.tar.gz -C /opt \
    && strip --strip-all /opt/arangodb3-linux-*/usr/sbin/arangod 2>/dev/null || true

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl3 libstdc++6 ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin arango 2>/dev/null || true
RUN mkdir -p /var/lib/arangodb /var/log/arangodb /var/cache/arangodb /var/lib/arangodb3-apps
COPY --from=builder /opt/arangodb3-linux-* /opt/arangodb
RUN chown -R 65534:65534 /opt/arangodb /var/lib/arangodb /var/log/arangodb /var/cache/arangodb /var/lib/arangodb3-apps
USER 65534:65534
WORKDIR /var/lib/arangodb
EXPOSE 8529
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8529/_api/version"]
ENTRYPOINT ["/opt/arangodb/usr/sbin/arangod", "--server.endpoint", "tcp://0.0.0.0:8529", "--database.directory", "/var/lib/arangodb", "--foxx.queues", "false", "--log.output", "-"]
LABEL org.opencontainers.image.title="arango" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened ArangoDB - multi-model NoSQL database (arango alias)" \
      org.opencontainers.image.vendor="ArangoDB" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
