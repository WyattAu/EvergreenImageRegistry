# =============================================================================
# EVERGREEN BASE - DEBIAN SLIM
# Minimal debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 reference image with hardening.
# This is the recommended fallback base for application images.
# =============================================================================


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates tzdata dumb-init 

RUN addgroup -S -g 65532 appuser 2>/dev/null || true && \
    adduser -u 65532 -G appuser -D -D -h /app -s /bin/false appuser 2>/dev/null || true
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="debian-slim" \
      org.opencontainers.image.description="Evergreen hardened debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 base image with ca-certificates, tzdata, dumb-init" \
      evergreen.image.tier="3" \
      evergreen.image.status="functional" \
      evergreen.image.category="base" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
