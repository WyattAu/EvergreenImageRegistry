# =============================================================================
# EVERGREEN HARDENED IMMICH-MACHINE-LEARNING
# Generated from template - Version: 1.106.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.106.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG GITHUB_TOKEN
RUN apk add --no-cache ca-certificates curl && \
    pip install --no-cache-dir --break-system-packages onnxruntime fastapi==0.115.0 uvicorn==0.30.0 pillow==10.4.0 numpy==2.1.0 scikit-learn 2>/dev/null || \
    pip install --no-cache-dir onnxruntime fastapi==0.115.0 uvicorn==0.30.0 pillow==10.4.0 numpy==2.1.0 scikit-learn || true && \
    adduser -u 65532 -D app 2>/dev/null || true && \
    mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 3003

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:3003/ || exit 1
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="immich-machine-learning" \
      org.opencontainers.image.description="immich-machine-learning container image" \
      org.opencontainers.image.version="1.106.0" \
      org.opencontainers.image.vendor="Immich" \
      org.opencontainers.image.source="https://github.com/immich-app/immich/releases" \
      evergreen.image.tier="3" \
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
