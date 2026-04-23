# =============================================================================
# SOVEREIGN HARDENED JUPYTER-ALL
# Generated from template - Version: 7.3.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.3.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache python3 py3-pip ca-certificates curl
RUN pip3 install --no-cache-dir --break-system-packages jupyter 2>/dev/null || \
    pip3 install --no-cache-dir jupyter
RUN useradd -m -u 65532 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8888
ENTRYPOINT ["jupyter"]
LABEL org.opencontainers.image.title="jupyter-all" \
      org.opencontainers.image.version="7.3.0" \
      org.opencontainers.image.vendor="Jupyter" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM