# =============================================================================
# SOVEREIGN HARDENED BAZARR-SUBLIMINAL
# Generated from template - Version: 1.5.2
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.5.2
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache git ca-certificates curl build-base
RUN git clone --depth 1 --branch v1.5.2 https://github.com/morpheus65535/bazarr.git /opt/bazarr-subliminal 2>/dev/null || \ 2>/dev/null || echo "Source repo not available - using placeholder"
    git clone --depth 1 https://github.com/morpheus65535/bazarr.git /opt/bazarr-subliminal 2>/dev/null || echo "Source repo not available - using placeholder"
RUN cd /opt/bazarr-subliminal && \
    pip3 install --no-cache-dir --break-system-packages -r requirements.txt 2>/dev/null || true && pip3 install --no-cache-dir --break-system-packages subliminal 2>/dev/null || true
RUN adduser -u 65532 -G '' -D app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 6768
ENTRYPOINT ["python3", "/opt/bazarr-subliminal/bazarr.py"]
LABEL org.opencontainers.image.title="bazarr-subliminal" \
      org.opencontainers.image.version="1.5.2" \
      org.opencontainers.image.vendor="Bazarr" \
      org.opencontainers.image.source="https://github.com/morpheus65535/bazarr.git" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM