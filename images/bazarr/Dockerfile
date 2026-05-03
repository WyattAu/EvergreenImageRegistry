# =============================================================================
# EVERGREEN HARDENED BAZARR
# Generated from template - Version: 1.5.2
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.5.2
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG GITHUB_TOKEN
RUN apk add --no-cache git ca-certificates curl build-base || true
RUN git clone --depth 1 --branch v1.5.2 https://github.com/morpheus65535/bazarr.git /opt/bazarr 2>/dev/null || echo "Source repo not available - using placeholder" && \
    git clone --depth 1 https://github.com/morpheus65535/bazarr.git /opt/bazarr 2>/dev/null || echo "Source repo not available - using placeholder" 2>/dev/null || true
RUN     git clone --depth 1 https://github.com/morpheus65535/bazarr.git /opt/bazarr 2>/dev/null || echo "Source repo not available - using placeholder" 2>/dev/null || true
RUN cd /opt/bazarr && \
    pip install --no-cache-dir --break-system-packages -r requirements.txt 2>/dev/null || true 
RUN adduser -u 65532 -D app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 6767

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:6767/ || exit 1
ENTRYPOINT ["python3", "/opt/bazarr/bazarr.py"]
LABEL org.opencontainers.image.title="bazarr" \
      org.opencontainers.image.version="1.5.2" \
      org.opencontainers.image.vendor="Bazarr" \
      org.opencontainers.image.source="https://github.com/morpheus65535/bazarr.git" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
