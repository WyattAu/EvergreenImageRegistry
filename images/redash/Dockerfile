# =============================================================================
# SOVEREIGN HARDENED REDASH
# Generated from template - Version: 10.0.0
# Constraint: debian-slim - Python runtime with web dependencies
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=10.0.0
ARG BUILD_DATE

FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    pip install --no-cache-dir --prefix=/install \
    redash=="${VERSION}" && \
    find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip libpq5 curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder /install /usr/local
RUN useradd -m -u 65534 -s /usr/sbin/nologin redash 2>/dev/null || true && \
    mkdir -p /app /var/log/redash /var/cache/redash && \
    chown -R 65534:65534 /app /var/log/redash /var/cache/redash
USER 65534:65534
WORKDIR /app
EXPOSE 5000
ENV REDASH_WEB_WORKERS="4"
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD ["curl", "-f", "http://localhost:5000/ping"]
ENTRYPOINT ["redash", "server"]
LABEL org.opencontainers.image.title="redash" \
      org.opencontainers.image.version="10.0.0" \
      org.opencontainers.image.description="Redash - Open Source Data Visualization and Dashboards" \
      org.opencontainers.image.vendor="Redash" \
      org.opencontainers.image.source="https://github.com/getredash/redash" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
