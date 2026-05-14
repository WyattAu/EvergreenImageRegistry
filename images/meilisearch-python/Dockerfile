# =============================================================================
# EVERGREEN HARDENED MEILISEARCH-PYTHON
# Generated from template - Version: 3.12
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.12
ARG TARGETARCH
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -D python 2>/dev/null || true && \
    mkdir -p /app /var/log/python /var/cache/python && chown -R python:python /app /var/log/python /var/cache/python 2>/dev/null || true
USER python
WORKDIR /app
EXPOSE 7700

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:7700/ || exit 1
ENTRYPOINT ["python"]
LABEL org.opencontainers.image.title="meilisearch-python" \
      org.opencontainers.image.description="meilisearch-python container image" \
      org.opencontainers.image.version="3.12" \
      org.opencontainers.image.vendor="Meilisearch" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/meilisearch/meilisearch-python"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
