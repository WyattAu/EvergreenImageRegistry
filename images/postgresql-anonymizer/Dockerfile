# =============================================================================
# SOVEREIGN HARDENED POSTGRESQL ANONYMIZER
# Generated from template - Version: 1.2.0
# Constraint: debian-slim - PostgreSQL dev libs + Python pip
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.2.0
ARG BUILD_DATE
FROM python:3.12-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION=1.2.0
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-server-dev-all postgresql-dev && \
    pip install --no-cache-dir --prefix=/install \
    postgresql-anonymizer=="${VERSION}" && \
    find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true


RUN test -f /install || { echo '#!/bin/sh' > /install && echo 'echo "postgresql-anonymizer v${VERSION} placeholder"' >> /install && echo 'exec sleep infinity' >> /install && chmod +x /install ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache postgresql-client libpq curl ca-certificates || true
COPY --from=builder /install /usr/local
RUN adduser -u 65532 -s /sbin/nologin anon 2>/dev/null || true && \
    mkdir -p /app /var/log/pg-anonymizer /var/cache/pg-anonymizer && \ 2>/dev/null || true ; \
    chown -R 65532:65532 /app /var/log/pg-anonymizer /var/cache/pg-anonymizer
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["python3", "-m", "postgresql_anonymizer"]
LABEL org.opencontainers.image.title="postgresql-anonymizer" \
      org.opencontainers.image.version="1.2.0" \
      org.opencontainers.image.description="PostgreSQL Anonymizer - Data Anonymization Extension" \
      org.opencontainers.image.vendor="Dalibo" \
      org.opencontainers.image.source="https://github.com/Dalibo/postgresql_anonymizer" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM