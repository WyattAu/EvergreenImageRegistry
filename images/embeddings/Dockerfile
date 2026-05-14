# =============================================================================
# EVERGREEN HARDENED EMBEDDINGS
# Generated from template - Version: 0.1.0
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.1.0
ARG TARGETARCH
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates curl && \
    adduser -u 65532 -D app 2>/dev/null || true && \
    mkdir -p /app /var/log/app /var/cache/app && chown -R app:app /app /var/log/app /var/cache/app 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["true"]
LABEL org.opencontainers.image.title="embeddings" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.vendor="Embeddings" \
      org.opencontainers.image.description="Placeholder - no upstream binary available" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/huggingface/transformers"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
