# =============================================================================
# SOVEREIGN PLACEHOLDER - KDB
# KDB+ is a proprietary in-memory columnar database by KX Systems.
# No public binaries or container images are available.
# This is a placeholder for license-managed deployments.
# =============================================================================

FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates tzdata libcurl4 && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN groupadd -g 65534 -r kdb 2>/dev/null || true && \
    useradd -r -u 65534 -g kdb -d /opt/kdb -s /sbin/nologin kdb 2>/dev/null || true && \
    mkdir -p /opt/kdb/data /opt/kdb/logs /var/log/kdb && \
    chown -R 65534:65534 /opt/kdb /var/log/kdb

USER 65534:65534
WORKDIR /opt/kdb
EXPOSE 5000
LABEL org.opencontainers.image.title="kdb" \
      org.opencontainers.image.description="Placeholder for KX Systems KDB+ proprietary database. Requires license." \
      org.opencontainers.image.vendor="KX Systems" \
      sovereign.image.tier="2" \
      sovereign.image.status="placeholder" \
      sovereign.image.category="database" \
      sovereign.image.note="KDB+ is proprietary. Copy licensed q binary to /opt/kdb/q before use." \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
