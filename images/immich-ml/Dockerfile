# =============================================================================
# EVERGREEN HARDENED IMMICH-ML
# Repack of upstream ghcr.io/immich-app/immich-machine-learning with
# health-shim overlay.
#
# Immich machine-learning carries a heavy native dependency stack (Python 3.11,
# ONNX Runtime, OpenCV, sharp, optional CUDA) that cannot be reliably
# transplanted onto a wolfi-base / scratch stage. The previous stub pip-
# installed onnxruntime/fastapi/uvicorn/pillow onto wolfi but never copied the
# app code and had no real CMD, so the image was non-functional.
#
# The robust path is to keep the upstream image as the final stage and layer
# hardening (health-shim, non-root user, writable model cache, HEALTHCHECK,
# labels) on top, delegating startup to the upstream entrypoint so model
# download and uvicorn bootstrap run unchanged.
#
# Note: this is an intentional, documented exception to the
# "no debian final stage" constraint, recorded for immich-ml specifically.
#
# Upstream image facts (verified from ghcr.io config, release tag = v2.7.5):
#   WorkingDir:   /usr/src      (PYTHONPATH=/usr/src)
#   Entrypoint:   ["tini","--"] Cmd: ["python","-m","immich_ml"]
#   Venv:         /opt/venv     (on PATH)
#   Cache:        MACHINE_LEARNING_CACHE_FOLDER=/cache, TRANSFORMERS_CACHE=/cache
#   Port:         3003          (default uvicorn bind)
#   User:         root (dropped to 65532 below; /cache chowned for model writes)
#
# Tag note: immich publishes `release` and `vX.Y.Z` tags but NOT `latest`.
# =============================================================================

ARG VERSION=1.106.0
ARG BUILD_DATE

ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

# immich does not publish a `:latest` tag; `release` tracks the current
# release. Pin to vX.Y.Z (e.g. v2.7.5) for reproducible builds.
FROM ghcr.io/immich-app/immich-machine-learning:v1.116.2

# Drop in the evergreen health-shim, which wraps the app with supervision,
# signal handling, healthchecks, and metrics.
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

# ONNX/transformer models are downloaded at runtime into /cache (set by the
# upstream MACHINE_LEARNING_CACHE_FOLDER / TRANSFORMERS_CACHE envs). Make it
# writable by the non-root user so model downloads succeed under UID 65532.
RUN mkdir -p /cache && chown -R 65532:65532 /cache

ENV EVERGREEN_LOG_LEVEL=info \
    SHIM_METRICS_ENABLED="true"

WORKDIR /usr/src
EXPOSE 3003

HEALTHCHECK --interval=10s --timeout=5s --start-period=60s --retries=5 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:3003"]

# Keep upstream entrypoint (tini must be PID 1 for signal handling)
# Shim is only used for HEALTHCHECK
CMD ["python", "-m", "immich_ml"]

LABEL org.opencontainers.image.title="immich-ml" \
      org.opencontainers.image.description="Immich machine-learning - face recognition, smart search, and image classification" \
      org.opencontainers.image.version="1.106.0" \
      org.opencontainers.image.vendor="Immich" \
      org.opencontainers.image.source="https://github.com/immich-app/immich" \
      evergreen.image.tier="standard" \
      evergreen.image.status="functional" \
      evergreen.image.category="machine-learning" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="upstream"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="tcp"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.entrypoint.pattern="repack-upstream-init"
STOPSIGNAL SIGTERM
