# =============================================================================
# SOVEREIGN HARDENED ELASTICSEARCH CURATOR
# Generated from template - Version: 5.8.3
# Constraint: debian-slim - Python runtime with ES client dependencies
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=5.8.3
ARG BUILD_DATE

FROM python:3.12-slim AS builder
RUN pip install --no-cache-dir --prefix=/install \
    elasticsearch-curator=="${VERSION}" && \
    find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder /install /usr/local
RUN useradd -m -u 65534 -s /usr/sbin/nologin curator 2>/dev/null || true && \
    mkdir -p /app /var/log/es-curator /var/cache/es-curator && \
    chown -R 65534:65534 /app /var/log/es-curator /var/cache/es-curator
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["curator", "--version"]
ENTRYPOINT ["curator"]
LABEL org.opencontainers.image.title="elasticsearch-curator" \
      org.opencontainers.image.version="5.8.3" \
      org.opencontainers.image.description="Elasticsearch Curator - Index Management Tool" \
      org.opencontainers.image.vendor="Elastic" \
      org.opencontainers.image.source="https://github.com/elastic/curator" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
