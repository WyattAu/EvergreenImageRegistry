# =============================================================================
# SOVEREIGN HARDENED REDASH
# Generated from template - Version: 10.0.0
# Constraint: debian-slim - Python runtime with web dependencies
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=10.0.0
ARG BUILD_DATE



RUN mkdir -p /install 2>/dev/null || true
FROM python:3.12-slim AS builder
ARG VERSION=10.0.0
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential postgresql-dev curl && \
    pip install --no-cache-dir --prefix=/install \
    redash=="${VERSION}" && \
    find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache libpq curl ca-certificates
COPY --from=builder /install /usr/local
RUN adduser -u 65532 -s /sbin/nologin redash 2>/dev/null || true && \
    mkdir -p /app /var/log/redash /var/cache/redash && \
    chown -R 65532:65532 /app /var/log/redash /var/cache/redash
USER 65532:65532
WORKDIR /app
EXPOSE 5000
ENV REDASH_WEB_WORKERS="4"
ENTRYPOINT ["redash", "server"]
LABEL org.opencontainers.image.title="redash" \
      org.opencontainers.image.version="10.0.0" \
      org.opencontainers.image.description="Redash - Open Source Data Visualization and Dashboards" \
      org.opencontainers.image.vendor="Redash" \
      org.opencontainers.image.source="https://github.com/getredash/redash" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM