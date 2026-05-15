# =============================================================================
# EVERGREEN HARDENED TVHEADEND
# Generated from template - Version: 4.3
# Constraint: debian-slim - system packages required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.3
ARG TARGETARCH
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -D hts 2>/dev/null || true && \
    mkdir -p /app /var/log/hts /var/cache/hts && chown -R hts:hts /app /var/log/hts /var/cache/hts 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 9981

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9981/ || exit 1
ENTRYPOINT ["tvheadend"]
LABEL org.opencontainers.image.title="tvheadend" \
      org.opencontainers.image.description="tvheadend container image" \
      org.opencontainers.image.version="4.3" \
      org.opencontainers.image.vendor="TVHeadend" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/tvheadend/tvheadend"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
