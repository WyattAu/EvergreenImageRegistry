# =============================================================================
# EVERGREEN HARDENED CHROMA
# Generated from template - Version: 0.5.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.5.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=0.5.0
RUN apk add --no-cache ca-certificates git build-base && \
    pip install --no-cache-dir --break-system-packages chromadb==${VERSION} 2>/dev/null || \
    pip install --no-cache-dir --break-system-packages chromadb && \
    adduser -u 65532 -D chroma 2>/dev/null || true && \
    mkdir -p /app /var/log/chroma /var/cache/chroma && chown -R chroma:chroma /app /var/log/chroma /var/cache/chroma 2>/dev/null || true
USER chroma
WORKDIR /app
EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8000"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="chroma" \
      org.opencontainers.image.description="chroma container image" \
      org.opencontainers.image.version="0.5.0" \
      org.opencontainers.image.vendor="Chroma" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/chroma-core/chroma"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
