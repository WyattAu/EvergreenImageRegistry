# =============================================================================
# EVERGREEN HARDENED GALLERY3
# Generated from template - Version: 3.0.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.0.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN apk add --no-cache git ca-certificates curl build-base && \
    git clone --branch v3.0.0 https://github.com/gallery/gallery3.git /opt/gallery3 2>/dev/null || { echo "Binary not available - download failed" >&2; exit 1; } && \
    git clone https://github.com/gallery/gallery3.git /opt/gallery3 2>/dev/null || { echo "Binary not available - download failed" >&2; exit 1; } 2>/dev/null && \
       git clone https://github.com/gallery/gallery3.git /opt/gallery3 2>/dev/null || { echo "Binary not available - download failed" >&2; exit 1; } 2>/dev/null && \
    cd /opt/gallery3 && \
    pip install --no-cache-dir --break-system-packages -r requirements.txt 2>/dev/null && \
    adduser -u 65532 -D app 2>/dev/null || true && \
    mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8000"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="gallery3" \
      org.opencontainers.image.description="gallery3 container image" \
      org.opencontainers.image.version="3.0.0" \
      org.opencontainers.image.vendor="Gallery" \
      org.opencontainers.image.source="https://github.com/gallery/gallery3.git" \
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
