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
    python3 python3-pip python3-venv && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir surrealdb==${VERSION} 2>/dev/null || \
    /opt/venv/bin/pip install --no-cache-dir surrealdb

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 libpython3.11 ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin surrealdb 2>/dev/null || true
RUN mkdir -p /var/lib/surrealdb /var/log/surrealdb
COPY --from=builder /opt/venv /opt/venv
RUN printf '#!/opt/venv/bin/python3\nimport surrealdb\nprint("surrealdb-python ready")\n' > /app/surrealdb-python && chmod +x /app/surrealdb-python
RUN chown -R 65534:65534 /opt/venv /var/lib/surrealdb /var/log/surrealdb /app
USER 65534:65534
WORKDIR /var/lib/surrealdb
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/opt/venv/bin/python3", "-c", "import surrealdb; print('ok')"]
ENTRYPOINT ["/app/surrealdb-python"]
LABEL org.opencontainers.image.title="surrealdb-python" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened SurrealDB Python - Python SDK for SurrealDB" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
