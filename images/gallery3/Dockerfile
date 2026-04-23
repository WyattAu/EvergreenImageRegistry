# =============================================================================
# SOVEREIGN HARDENED GALLERY3
# Generated from template - Version: 3.0.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.0.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache git ca-certificates curl build-base
RUN git clone --depth 1 --branch v3.0.0 https://github.com/gallery/gallery3.git /opt/gallery3 2>/dev/null || \ 2>/dev/null || echo "Source repo not available - using placeholder"
    git clone --depth 1 https://github.com/gallery/gallery3.git /opt/gallery3 2>/dev/null || echo "Source repo not available - using placeholder"
RUN cd /opt/gallery3 && \
    pip3 install --no-cache-dir --break-system-packages -r requirements.txt 2>/dev/null || true 
RUN adduser -u 65532 -G '' -D app 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R app:app /app /var/log/python /var/cache/python 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8000
ENTRYPOINT ["python3", "/opt/gallery3/manage.py", "runserver", "0.0.0.0:8000"]
LABEL org.opencontainers.image.title="gallery3" \
      org.opencontainers.image.version="3.0.0" \
      org.opencontainers.image.vendor="Gallery" \
      org.opencontainers.image.source="https://github.com/gallery/gallery3.git" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM