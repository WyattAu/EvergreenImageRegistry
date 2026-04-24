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
    curl ca-certificates gnupg apt-transport-https && \
    curl --retry 3 --retry-delay 5 -fsSL "https://downloads.scylladb.com/deb/debian/scylladb-${VERSION%.*}-list.gnupg" -o /etc/apt/trusted.gnupg.d/scylladb.gnupg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/trusted.gnupg.d/scylladb.gnupg] http://downloads.scylladb.com/deb/debian bookworm main" \       > /etc/apt/sources.list.d/scylladb.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends scylla \
    && rm -rf /var/lib/apt/lists/*

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates libxml2-utils python3 systemd
RUN adduser -u 65532 -s /sbin/nologin scylla 2>/dev/null || true
RUN mkdir -p /var/lib/scylla /var/log/scylla
COPY --from=builder /opt/scylladb /opt/scylladb
COPY --from=builder /usr/bin/scylla /usr/bin/scylla
COPY --from=builder /usr/lib/scylla /usr/lib/scylla 2>/dev/null || true
COPY --from=builder /etc/scylla /etc/scylla 2>/dev/null || true
USER 65532:65532
WORKDIR /var/lib/scylla
EXPOSE 9042 9160 10000
ENTRYPOINT ["/usr/bin/scylla"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      org.opencontainers.image.title="scylladb" \
      org.opencontainers.image.description="Sovereign hardened ScyllaDB - high-performance NoSQL database compatible with Cassandra" \
      org.opencontainers.image.version="${VERSION}"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM