# =============================================================================
# SOVEREIGN HARDENED LITELLM-PROXY
# Generated from template - Version: 1.60.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.60.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates curl
RUN pip3 install --no-cache-dir --break-system-packages litellm[proxy] 2>/dev/null || \
    pip3 install --no-cache-dir litellm[proxy]
RUN adduser -u 65532 -D app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 4000
ENTRYPOINT ["litellm"]
LABEL org.opencontainers.image.title="litellm-proxy" \
      org.opencontainers.image.version="1.60.0" \
      org.opencontainers.image.vendor="LiteLLM" \
      org.opencontainers.image.source="https://github.com/BerriAI/litellm" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM