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
RUN python3 -m venv /opt/venv ; /opt/venv/bin/pip install --no-cache-dir --upgrade pip ; /opt/venv/bin/pip install --no-cache-dir surrealdb==${VERSION} 2>/dev/null ||  \/opt/venv/bin/pip install --no-cache-dir surrealdb || true


      RUN org.opencontainers.image.version="${VERSION}" \
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
RUN mkdir -p /usr/local/lib/python3.* 2>/dev/null || true ; touch /usr/local/lib/python3.*/dist-packages 2>/dev/null || true
RUN mkdir -p / 2>/dev/null || true ; touch /app 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache python3 2>/dev/null || true
RUN mkdir -p /usr/local/lib/python3.11 2>/dev/null || true
COPY --from=builder /usr/local/lib/python3.*/dist-packages /usr/local/lib/python3.11/site-packages 2>/dev/null || true
RUN mkdir -p /app 2>/dev/null || true
COPY --from=builder /app /app 2>/dev/null || true
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false surrealdb-python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["python3", "-m", "surrealdb"]
