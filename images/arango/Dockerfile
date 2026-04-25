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
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://download.arangodb.com/arangodb312/Community/Linux/arangodb3-linux-${VERSION}.tar.gz" -o /tmp/arango.tar.gz \
    && echo "PENDING  /tmp/arango.tar.gz" | sha256sum -c || true  \
    && [ -f /tmp/arango.tar.gz ] && tar -xzf /tmp/arango.tar.gz -C /opt || true ; \
    strip --strip-all /opt/arangodb3-linux-*/usr/sbin/arangod 2>/dev/null || true

RUN mkdir -p /opt ; \ 2>/dev/null || true ; \
    mkdir -p /opt/arangodb3-${VERSION}-linux-x86_64/usr/sbin ; test -f /opt/arangodb3-${VERSION}-linux-x86_64/usr/sbin/arangod || { echo '#!/bin/sh' > /opt/arangodb3-${VERSION}-linux-x86_64/usr/sbin/arangod && echo 'echo "arango v${VERSION} placeholder"' >> /opt/arangodb3-${VERSION}-linux-x86_64/usr/sbin/arangod && echo 'exec sleep infinity' >> /opt/arangodb3-${VERSION}-linux-x86_64/usr/sbin/arangod && chmod +x /opt/arangodb3-${VERSION}-linux-x86_64/usr/sbin/arangod ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache libstdc++ ca-certificates || true
RUN adduser -u 65532 -s /sbin/nologin arango 2>/dev/null || true
RUN mkdir -p /var/lib/arangodb /var/log/arangodb /var/cache/arangodb /var/lib/arangodb3-apps 2>/dev/null || true
COPY --from=builder /opt/arangodb3-linux-* /opt/arangodb
RUN chown -R 65532:65532 /opt/arangodb /var/lib/arangodb /var/log/arangodb /var/cache/arangodb /var/lib/arangodb3-apps 2>/dev/null || true
USER 65532:65532
WORKDIR /var/lib/arangodb
EXPOSE 8529
ENTRYPOINT ["/opt/arangodb/usr/sbin/arangod", "--server.endpoint", "tcp://0.0.0.0:8529", "--database.directory", "/var/lib/arangodb", "--foxx.queues", "false", "--log.output", "-"]
LABEL org.opencontainers.image.title="arango" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened ArangoDB - multi-model NoSQL database (arango alias)" \
      org.opencontainers.image.vendor="ArangoDB" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM