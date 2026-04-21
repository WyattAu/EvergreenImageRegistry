# =============================================================================
# SOVEREIGN HARDENED SCYLLADB
# Generated from template - Version: 5.4.6
# Constraint: debian-slim - ScyllaDB requires glibc + system libraries
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.4.6
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg2 apt-transport-https && \
    curl -fsSL "https://downloads.scylladb.com/deb/debian/scylladb-${VERSION%.*}-list.gpg" -o /etc/apt/trusted.gpg.d/scylladb.gpg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/scylladb.gpg] http://downloads.scylladb.com/deb/debian bookworm main" \
       > /etc/apt/sources.list.d/scylladb.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends scylla \
    && rm -rf /var/lib/apt/lists/*

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates libxml2-utils python3 systemd && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin scylla 2>/dev/null || true
RUN mkdir -p /var/lib/scylla /var/log/scylla
COPY --from=builder /opt/scylladb /opt/scylladb
COPY --from=builder /usr/bin/scylla /usr/bin/scylla
COPY --from=builder /usr/lib/scylla /usr/lib/scylla 2>/dev/null || true
COPY --from=builder /etc/scylla /etc/scylla 2>/dev/null || true
USER 65534:65534
WORKDIR /var/lib/scylla
EXPOSE 9042 9160 10000
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["/usr/bin/scylla", "--version"]
ENTRYPOINT ["/usr/bin/scylla"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      org.opencontainers.image.title="scylladb" \
      org.opencontainers.image.description="Sovereign hardened ScyllaDB - high-performance NoSQL database compatible with Cassandra" \
      org.opencontainers.image.version="${VERSION}"
