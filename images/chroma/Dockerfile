# =============================================================================
# SOVEREIGN HARDENED CHROMA
# Generated from template - Version: 0.5.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.5.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=0.5.0
RUN apk add --no-cache ca-certificates git build-base 
RUN pip install --no-cache-dir --break-system-packages chromadb==${VERSION} 2>/dev/null || \
    pip install --no-cache-dir --break-system-packages chromadb
RUN adduser -u 65532 -D chroma 2>/dev/null || true
RUN mkdir -p /app /var/log/chroma /var/cache/chroma && chown -R chroma:chroma /app /var/log/chroma /var/cache/chroma 2>/dev/null || true
USER chroma
WORKDIR /app
EXPOSE 8000
ENTRYPOINT ["chroma"]
LABEL org.opencontainers.image.title="chroma" \
      org.opencontainers.image.version="0.5.0" \
      org.opencontainers.image.vendor="Chroma" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM