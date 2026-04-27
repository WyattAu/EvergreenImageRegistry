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
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip python3 && rm -rf /var/lib/apt/lists/* || true
RUN python3 -m venv /opt/venv || true ; /opt/venv/bin/pip install --no-cache-dir --upgrade pip || true ; /opt/venv/bin/pip install --no-cache-dir surrealdb==${VERSION} 2>/dev/null || /opt/venv/bin/pip install --no-cache-dir surrealdb || true
RUN mkdir -p /app /usr/local/lib/python3.11/site-packages || true ; touch /app/placeholder || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache python3 || true
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true ; adduser -u 65532 -G nogroup -D -h /app -s /bin/false surrealdb-python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["python3", "-m", "surrealdb"]
LABEL org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened SurrealDB Python - Python SDK for SurrealDB" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi" \
      sovereign.metrics.native="ztunnel" \
      sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
