# =============================================================================
# SOVEREIGN META - UPSTREAM
# This is a metadata directory for upstream references, not a container image.
# =============================================================================


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates 
LABEL org.opencontainers.image.title="upstream" \
      org.opencontainers.image.description="Meta directory for upstream version tracking. Not a runnable container." \
      sovereign.image.tier="3" \
      sovereign.image.status="reference" \
      sovereign.image.category="meta" \
      sovereign.image.note="Upstream tracking directory, not a container image."

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
