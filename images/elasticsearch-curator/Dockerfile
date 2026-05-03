# =============================================================================
# EVERGREEN HARDENED ELASTICSEARCH CURATOR
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


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache curl ca-certificates 
COPY --from=builder /install /usr/local
RUN adduser -u 65532 -s /bin/false curator 2>/dev/null || true && \
    mkdir -p /app /var/log/es-curator /var/cache/es-curator ; \
    chown -R 65532:65532 /app /var/log/es-curator /var/cache/es-curator
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["curator"]
LABEL org.opencontainers.image.title="elasticsearch-curator" \
      org.opencontainers.image.version="5.8.3" \
      org.opencontainers.image.description="Elasticsearch Curator - Index Management Tool" \
      org.opencontainers.image.vendor="Elastic" \
      org.opencontainers.image.source="https://github.com/elastic/curator" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
