# =============================================================================
# SOVEREIGN HARDENED JUPYTER-SCIKIT
# Generated from template - Version: 7.3.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.3.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates curl 
RUN pip install --no-cache-dir --break-system-packages jupyterlab scikit-learn pandas numpy matplotlib 2>/dev/null || \
    pip install --no-cache-dir jupyterlab scikit-learn pandas numpy matplotlib || true
RUN adduser -u 65532 -D app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8888
ENTRYPOINT ["jupyter-lab"]
LABEL org.opencontainers.image.title="jupyter-scikit" \
      org.opencontainers.image.version="7.3.0" \
      org.opencontainers.image.vendor="Jupyter" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM