# =============================================================================
# SOVEREIGN HARDENED LANGSERVE
# Generated from template - Version: 0.3.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.3.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
ARG GITHUB_TOKEN
RUN apk add --no-cache ca-certificates curl 
RUN pip install --no-cache-dir --break-system-packages langserve 2>/dev/null || \
    pip install --no-cache-dir langserve
RUN adduser -u 65532 -D app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8000
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="langserve" \
      org.opencontainers.image.version="0.3.0" \
      org.opencontainers.image.vendor="LangServe" \
      org.opencontainers.image.source="https://github.com/langchain-ai/langserve" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM