# =============================================================================
# SOVEREIGN HARDENED PREFECT-SERVER
# Generated from template - Version: 3.3.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.3.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
ARG GITHUB_TOKEN
RUN apk add --no-cache ca-certificates curl 
RUN pip install --no-cache-dir --break-system-packages prefect 2>/dev/null || \
    pip install --no-cache-dir prefect || true
RUN adduser -u 65532 -D app || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python
USER 65532:65532
WORKDIR /app
EXPOSE 4200
ENTRYPOINT ["prefect"]
LABEL org.opencontainers.image.title="prefect-server" \
      org.opencontainers.image.version="3.3.0" \
      org.opencontainers.image.vendor="Prefect" \
      org.opencontainers.image.source="https://github.com/PrefectHQ/prefect" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
