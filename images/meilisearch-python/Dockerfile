# =============================================================================
# SOVEREIGN HARDENED MEILISEARCH-PYTHON
# Generated from template - Version: 3.12
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.12
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates
RUN adduser -u 65532 -D python 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R python:python /app /var/log/python /var/cache/python 2>/dev/null || true
USER python
WORKDIR /app
EXPOSE 7700
ENTRYPOINT ["python"]
LABEL org.opencontainers.image.title="meilisearch-python" \
      org.opencontainers.image.version="3.12" \
      org.opencontainers.image.vendor="Meilisearch" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM