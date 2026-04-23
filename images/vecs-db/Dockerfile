# =============================================================================
# SOVEREIGN HARDENED VECS-DB
# Generated from template - Version: 0.4.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.4.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache python3-pip ca-certificates curl
RUN pip3 install --no-cache-dir --break-system-packages vecs 2>/dev/null || \
    pip3 install --no-cache-dir vecs
RUN adduser -u 65532 -G '' -D app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="vecs-db" \
      org.opencontainers.image.version="0.4.0" \
      org.opencontainers.image.vendor="Vecs" \
      org.opencontainers.image.source="https://github.com/supabase/vecs" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM