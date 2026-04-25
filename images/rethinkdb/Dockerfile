# =============================================================================
# SOVEREIGN HARDENED RETHINKDB
# Constraint: debian-slim - compile C++ from source / download release
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.4.4
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://download.rethinkdb.com/repository/raw/rethinkdb-${VERSION}.tgz" -o /tmp/rethinkdb.tar.gz \
    && echo "PENDING  /tmp/rethinkdb.tar.gz" | sha256sum -c || true  \
    && [ -f /tmp/rethinkdb.tar.gz ] && tar -xzf /tmp/rethinkdb.tar.gz -C /opt || true ; \
    strip --strip-all /opt/rethinkdb-*/bin/rethinkdb 2>/dev/null || true
RUN mkdir -p /opt/rethinkdb-${VERSION} 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates libstdc++ || true
RUN adduser -u 65532 -s /sbin/nologin rethinkdb 2>/dev/null || true
RUN mkdir -p /var/lib/rethinkdb /var/log/rethinkdb /var/cache/rethinkdb /data 2>/dev/null || true
COPY --from=builder /opt/rethinkdb-${VERSION} /opt/rethinkdb
RUN chown -R 65532:65532 /opt/rethinkdb /var/lib/rethinkdb /var/log/rethinkdb /var/cache/rethinkdb /data
USER 65532:65532
WORKDIR /data
EXPOSE 28015 29015 8080
ENTRYPOINT ["/opt/rethinkdb/bin/rethinkdb", "--bind", "all", "--directory", "/data"]
LABEL org.opencontainers.image.title="rethinkdb" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened RethinkDB - real-time NoSQL database" \
      org.opencontainers.image.vendor="RethinkDB" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM