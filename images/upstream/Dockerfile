# =============================================================================
# EVERGREEN META - UPSTREAM
# This is a metadata directory for upstream references, not a container image.
# =============================================================================


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates 
LABEL org.opencontainers.image.title="upstream" \
      org.opencontainers.image.description="Meta directory for upstream version tracking. Not a runnable container." \
      evergreen.image.tier="3" \
      evergreen.image.status="reference" \
      evergreen.image.category="meta" \
      evergreen.image.note="Upstream tracking directory, not a container image." \
            org.opencontainers.image.source="https://github.com/WyattAu/EvergreenImageRegistry" \
                  org.opencontainers.image.version="unknown"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
