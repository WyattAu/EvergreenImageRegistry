# =============================================================================
# EVERGREEN HARDENED MLFLOW-TRACKING
# Generated from template - Version: 2.21.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.21.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG GITHUB_TOKEN
RUN apk add --no-cache ca-certificates curl && \
    pip install --no-cache-dir --break-system-packages mlflow 2>/dev/null || \
    pip install --no-cache-dir mlflow || true && \
    adduser -u 65532 -D app 2>/dev/null || true && \
    mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:5000/ || exit 1
ENTRYPOINT ["mlflow"]
LABEL org.opencontainers.image.title="mlflow-tracking" \
      org.opencontainers.image.description="mlflow-tracking container image" \
      org.opencontainers.image.version="2.21.0" \
      org.opencontainers.image.vendor="MLflow" \
      org.opencontainers.image.source="https://github.com/mlflow/mlflow" \
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
