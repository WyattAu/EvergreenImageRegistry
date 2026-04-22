# =============================================================================
# SOVEREIGN PLACEHOLDER - KDB+
# KDB+ Plus edition (proprietary, requires KX Systems license).
# Enhanced version with additional features over base KDB.
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
LABEL org.opencontainers.image.title="kdb-plus" \
      org.opencontainers.image.description="Placeholder for KX Systems KDB+ Plus edition. Requires license." \
      org.opencontainers.image.vendor="KX Systems" \
      sovereign.image.tier="2" \
      sovereign.image.status="placeholder" \
      sovereign.image.category="database" \
      sovereign.image.note="KDB+ Plus is proprietary. Copy licensed q binary to /opt/kdb/q before use." \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
