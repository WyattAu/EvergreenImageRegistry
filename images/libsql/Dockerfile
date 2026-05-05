# =============================================================================
# EVERGREEN HARDENED LIBSQL-SERVER
# Turso's open-source SQLite fork with networking (libSQL server)
# https://github.com/tursodatabase/libsql
# =============================================================================

ARG VERSION=0.24.32
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31 AS builder
ARG VERSION
RUN apk add --no-cache ca-certificates curl xz && \
    curl --retry 3 --retry-delay 5 -fSL "https://github.com/tursodatabase/libsql/releases/download/libsql-server-v${VERSION}/libsql-server-x86_64-unknown-linux-gnu.tar.xz" -o /tmp/libsql-server.tar.xz \
    && echo "71720fc8648c19efef416efebd47145ef59b62e198770533530a858e1336879f  /tmp/libsql-server.tar.xz" | sha256sum -c -
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION
ARG BUILD_DATE
RUN apk add --no-cache ca-certificates tzdata libgcc
COPY --from=builder /tmp/libsql-server.tar.xz /tmp/libsql-server.tar.xz
RUN addgroup -S -g 65532 libsql 2>/dev/null || true && \
    adduser -u 65532 -G libsql -D -h /opt/libsql -s /bin/false libsql 2>/dev/null || true && \
    mkdir -p /opt/libsql /var/lib/libsql && \
    cd /opt/libsql && tar xJf /tmp/libsql-server.tar.xz && rm -f /tmp/libsql-server.tar.xz && \
    chown -R 65532:65532 /opt/libsql /var/lib/libsql

USER 65532:65532
WORKDIR /var/lib/libsql
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["/opt/libsql/libsql-server"]
LABEL org.opencontainers.image.title="libsql-server" \
      org.opencontainers.image.description="Turso libSQL server - open-source SQLite fork with networking" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.source="https://github.com/tursodatabase/libsql" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="prometheus"
LABEL evergreen.health.type="http"
LABEL evergreen.health.path="/health"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
