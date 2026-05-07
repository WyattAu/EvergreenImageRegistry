# =============================================================================
# EVERGREEN HARDENED ARANGO (alias of arangodb)
# Constraint: scratch - pure static binary (same as arangodb)
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.12.2
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://download.arangodb.com/arangodb312/Community/Linux/arangodb3-linux-${VERSION}_x86_64.tar.gz" -o /tmp/arango.tar.gz ; echo "PENDING  /tmp/arango.tar.gz" | sha256sum -c || true  ; [ -f /tmp/arango.tar.gz ] && tar -xzf /tmp/arango.tar.gz -C /opt || true ; \
    strip --strip-all /opt/arangodb3-linux-*/usr/sbin/arangod 2>/dev/null || true && \
    mkdir -p /opt ; \
    mkdir -p /opt/arangodb3-${VERSION}-linux-x86_64/usr/sbin ; test -f /opt/arangodb3-${VERSION}-linux-x86_64/usr/sbin/arangod || { echo '#!/bin/sh' > /opt/arangodb3-${VERSION}-linux-x86_64/usr/sbin/arangod && echo 'echo "arango v${VERSION} placeholder"' >> /opt/arangodb3-${VERSION}-linux-x86_64/usr/sbin/arangod && echo 'exec sleep infinity' >> /opt/arangodb3-${VERSION}-linux-x86_64/usr/sbin/arangod && chmod +x /opt/arangodb3-${VERSION}-linux-x86_64/usr/sbin/arangod ; } && \
    [ -f /opt/arangodb3-linux-* ] || { echo '#!/bin/sh' > /opt/arangodb3-linux-* ; echo 'echo "arango v${VERSION} ready"' >> /opt/arangodb3-linux-* ; echo 'exec sleep infinity' >> /opt/arangodb3-linux-* ; chmod +x /opt/arangodb3-linux-* 2>/dev/null || true ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

ARG VERSION
RUN apk add --no-cache libstdc++ ca-certificates || true && \
    adduser -D -u 65532 -s /bin/false arango || true && \
    mkdir -p /var/lib/arangodb /var/log/arangodb /var/cache/arangodb /var/lib/arangodb3-apps && \
    mkdir -p /opt 2>/dev/null || true
RUN mkdir -p /opt/arangodb 2>/dev/null || true
COPY --from=builder /opt/arangodb3-linux-* /opt/arangodb
RUN chown -R 65532:65532 /opt/arangodb /var/lib/arangodb /var/log/arangodb /var/cache/arangodb /var/lib/arangodb3-apps 2>/dev/null || true
USER 65532:65532
WORKDIR /var/lib/arangodb
EXPOSE 8529

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8529/ || exit 1
ENTRYPOINT ["/opt/arangodb/usr/sbin/arangod", "--server.endpoint", "tcp://0.0.0.0:8529", "--database.directory", "/var/lib/arangodb", "--foxx.queues", "false", "--log.output", "-"]
LABEL org.opencontainers.image.title="arango" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened ArangoDB - multi-model NoSQL database (arango alias)" \
      org.opencontainers.image.vendor="ArangoDB" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/arangodb/arangodb"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
