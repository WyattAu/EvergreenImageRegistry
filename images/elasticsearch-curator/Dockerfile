# =============================================================================
# SOVEREIGN HARDENED ELASTICSEARCH CURATOR
# Generated from template - Version: 5.8.3
# Constraint: debian-slim - Python runtime with ES client dependencies
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=5.8.3
ARG BUILD_DATE
FROM python:3.12-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION=5.8.3
RUN pip install --no-cache-dir --prefix=/install \
    elasticsearch-curator=="${VERSION}" && \
    find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache curl ca-certificates || true
COPY --from=builder /install /usr/local
RUN adduser -u 65532 -s /sbin/nologin curator 2>/dev/null || true && \
    mkdir -p /app /var/log/es-curator /var/cache/es-curator ; \
    chown -R 65532:65532 /app /var/log/es-curator /var/cache/es-curator
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["curator"]
LABEL org.opencontainers.image.title="elasticsearch-curator" \
      org.opencontainers.image.version="5.8.3" \
      org.opencontainers.image.description="Elasticsearch Curator - Index Management Tool" \
      org.opencontainers.image.vendor="Elastic" \
      org.opencontainers.image.source="https://github.com/elastic/curator" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM