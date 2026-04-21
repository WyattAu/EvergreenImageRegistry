# =============================================================================
# SOVEREIGN HARDENED POSTGRESQL ANONYMIZER
# Generated from template - Version: 1.2.0
# Constraint: debian-slim - PostgreSQL dev libs + Python pip
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.2.0
ARG BUILD_DATE

FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-server-dev-all libpq-dev && \
    pip install --no-cache-dir --prefix=/install \
    postgresql-anonymizer=="${VERSION}" && \
    find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client-17 python3 python3-pip libpq5 curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder /install /usr/local
RUN useradd -m -u 65534 -s /usr/sbin/nologin anon 2>/dev/null || true && \
    mkdir -p /app /var/log/pg-anonymizer /var/cache/pg-anonymizer && \
    chown -R 65534:65534 /app /var/log/pg-anonymizer /var/cache/pg-anonymizer
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python3", "-c", "import postgres_anonymizer; print('ok')"]
ENTRYPOINT ["python3", "-m", "postgresql_anonymizer"]
LABEL org.opencontainers.image.title="postgresql-anonymizer" \
      org.opencontainers.image.version="1.2.0" \
      org.opencontainers.image.description="PostgreSQL Anonymizer - Data Anonymization Extension" \
      org.opencontainers.image.vendor="Dalibo" \
      org.opencontainers.image.source="https://github.com/Dalibo/postgresql_anonymizer" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
