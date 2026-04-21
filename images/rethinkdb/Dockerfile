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
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://download.rethinkdb.com/repository/raw/rethinkdb-${VERSION}.tgz" -o /tmp/rethinkdb.tar.gz \
    && echo "PENDING  /tmp/rethinkdb.tar.gz" | sha256sum -c - \
    && tar -xzf /tmp/rethinkdb.tar.gz -C /opt \
    && strip --strip-all /opt/rethinkdb-*/bin/rethinkdb 2>/dev/null || true

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    libprotobuf32 libssl3 ca-certificates libstdc++6 && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin rethinkdb 2>/dev/null || true
RUN mkdir -p /var/lib/rethinkdb /var/log/rethinkdb /var/cache/rethinkdb /data
COPY --from=builder /opt/rethinkdb-${VERSION} /opt/rethinkdb
RUN chown -R 65534:65534 /opt/rethinkdb /var/lib/rethinkdb /var/log/rethinkdb /var/cache/rethinkdb /data
USER 65534:65534
WORKDIR /data
EXPOSE 28015 29015 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8080"]
ENTRYPOINT ["/opt/rethinkdb/bin/rethinkdb", "--bind", "all", "--directory", "/data"]
LABEL org.opencontainers.image.title="rethinkdb" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened RethinkDB - real-time NoSQL database" \
      org.opencontainers.image.vendor="RethinkDB" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
