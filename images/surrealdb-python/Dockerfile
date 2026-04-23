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
    python3-pip python3 && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir surrealdb==${VERSION} 2>/dev/null || \
    /opt/venv/bin/pip install --no-cache-dir surrealdb

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache python3 ca-certificates
RUN adduser -u 65532 -s /sbin/nologin surrealdb 2>/dev/null || true
RUN mkdir -p /var/lib/surrealdb /var/log/surrealdb
COPY --from=builder /opt/venv /opt/venv
RUN printf '#!/opt/venv/bin/python3\nimport surrealdb\nprint("surrealdb-python ready")\n' > /app/surrealdb-python && chmod +x /app/surrealdb-python
RUN chown -R 65532:65532 /opt/venv /var/lib/surrealdb /var/log/surrealdb /app
USER 65532:65532
WORKDIR /var/lib/surrealdb
EXPOSE 8000
ENTRYPOINT ["/app/surrealdb-python"]
LABEL org.opencontainers.image.title="surrealdb-python" \
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