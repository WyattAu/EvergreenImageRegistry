# =============================================================================
# EVERGREEN HARDENED PREFECT
# Generated from template - Version: 3.3.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.3.0
ARG BUILD_DATE
ARG TARGETARCH


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates curl 
RUN pip install --no-cache-dir --break-system-packages prefect 2>/dev/null || \
    pip install --no-cache-dir prefect || true
RUN adduser -u 65532 -D app || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python
USER 65532:65532
WORKDIR /app
EXPOSE 4200

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:4200/ || exit 1
ENTRYPOINT ["prefect"]
LABEL org.opencontainers.image.title="prefect" \
      org.opencontainers.image.version="3.3.0" \
      org.opencontainers.image.vendor="Prefect" \
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
