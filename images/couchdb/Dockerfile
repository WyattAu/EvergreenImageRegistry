# =============================================================================
# SOVEREIGN HARDENED COUCHDB
# Generated from template - Version: 3.3.3
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.3.3
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates erlang-base erlang-dev erlang-nox libmozjs78-dev && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL -k "https://dlcdn.apache.org/couchdb/source/${VERSION}/apache-couchdb-${VERSION}.tar.gz" -o /tmp/couchdb.tar.gz && \
    tar -xzf /tmp/couchdb.tar.gz -C /tmp && \
    cd /tmp/apache-couchdb-${VERSION} && \
    ./configure --prefix=/opt/couchdb && \
    make release && \
    cp -a rel/couchdb /opt/couchdb && \
    rm -rf /tmp/couchdb.tar.gz /tmp/apache-couchdb-${VERSION}

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    erlang-base erlang-nox libmozjs78-0 ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' couchdb 2>/dev/null || true
RUN mkdir -p /app /var/log/couchdb /var/cache/couchdb && chown -R couchdb:couchdb /app /var/log/couchdb /var/cache/couchdb 2>/dev/null || true
USER couchdb
WORKDIR /app
COPY --from=downloader /opt/couchdb /opt/couchdb
EXPOSE 5984
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:5984
ENTRYPOINT ["/opt/couchdb/bin/couchdb"]
LABEL org.opencontainers.image.title="couchdb" \
      org.opencontainers.image.version="3.3.3" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
