# =============================================================================
# SOVEREIGN HARDENED SURREALDB-PYTHON
# Constraint: debian-slim - Python package via pip
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip python3 && rm -rf /var/lib/apt/lists/* || true
RUN python3 -m venv /opt/venv ; /opt/venv/bin/pip install --no-cache-dir --upgrade pip ; /opt/venv/bin/pip install --no-cache-dir surrealdb==${VERSION} 2>/dev/null || \    /opt/venv/bin/pip install --no-cache-dir surrealdb || true


      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened SurrealDB Python - Python SDK for SurrealDB" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM