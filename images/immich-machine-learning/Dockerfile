# =============================================================================
# EVERGREEN HARDENED IMMICH-MACHINE-LEARNING
# Generated from template - Version: 2.7.5
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.7.5
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN apk add --no-cache ca-certificates curl && \
    pip install --no-cache-dir --break-system-packages onnxruntime fastapi==0.115.0 uvicorn==0.30.0 pillow==10.4.0 numpy==2.1.0 scikit-learn 2>/dev/null || \
    pip install --no-cache-dir onnxruntime fastapi==0.115.0 uvicorn==0.30.0 pillow==10.4.0 numpy==2.1.0 scikit-learn && \
    adduser -u 65532 -D app 2>/dev/null || true && \
    mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 3003

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:3003"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "python3 -m gunicorn.main"]
LABEL org.opencontainers.image.title="immich-machine-learning" \
      org.opencontainers.image.description="immich-machine-learning container image" \
      org.opencontainers.image.version="2.7.5" \
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
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
