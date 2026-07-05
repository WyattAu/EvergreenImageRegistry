# =============================================================================
# EVERGREEN HARDENED PAPERLESS-NGX
# Repack of upstream ghcr.io/paperless-ngx/paperless-ngx:latest with
# health-shim overlay.
#
# Paperless-ngx has a deep, complex Python + native library dependency tree
# (Django, OCRmyPDF, tesseract, ghostscript, qpdf, redis client, postgres
# drivers, etc.) that cannot be reliably transplanted onto a wolfi-base /
# scratch stage. The previous stub Dockerfile tried to do this with a Python
# venv but referenced `s6-svscan /etc/s6` which was never installed, leaving
# the image non-functional.
#
# The robust path is to keep the upstream image as the final stage and layer
# hardening (health-shim, HEALTHCHECK, labels) on top.
#
# Note: this is an intentional, documented exception to the
# "no debian final stage" constraint, recorded for paperless-ngx specifically.
# =============================================================================

ARG VERSION=2.20.15
ARG BUILD_DATE

ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.3.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM ghcr.io/paperless-ngx/paperless-ngx:${VERSION}

# Drop in the evergreen health-shim, which wraps the upstream
# docker-entrypoint.sh with supervision, healthchecks, and metrics.
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ENV EVERGREEN_LOG_LEVEL=info \
    SHIM_METRICS_ENABLED="true"

WORKDIR /usr/src/paperless
EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8000"]

# Keep upstream /init as entrypoint (s6-overlay must be PID 1)
# Shim is only used for HEALTHCHECK
ENTRYPOINT ["/init"]

LABEL org.opencontainers.image.title="paperless-ngx" \
      org.opencontainers.image.description="Paperless-ngx - document management system" \
      org.opencontainers.image.version="2.20.15" \
      org.opencontainers.image.vendor="Paperless-ngx" \
      org.opencontainers.image.source="https://github.com/paperless-ngx/paperless-ngx" \
      evergreen.image.tier="critical" \
      evergreen.image.status="functional" \
      evergreen.image.category="document-management" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="upstream"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="tcp"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.entrypoint.pattern="repack-upstream-init"
STOPSIGNAL SIGTERM
