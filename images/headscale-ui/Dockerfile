# Evergreen hardened headscale-ui
# Repack of upstream gurucomputing/headscale-ui with health-shim overlay
ARG SHIM_VERSION=v1.3.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM ghcr.io/gurucomputing/headscale-ui:2026.03.17

USER root
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

USER appuser

ENV SHIM_METRICS_ENABLED="true"
EXPOSE 80 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

LABEL org.opencontainers.image.title="headscale-ui" \
      org.opencontainers.image.description="Headscale UI - web interface for Headscale" \
      org.opencontainers.image.version="2026.03.17" \
      org.opencontainers.image.vendor="Guru Computing" \
      org.opencontainers.image.source="https://github.com/gurucomputing/headscale-ui" \
      evergreen.image.tier="2"
LABEL evergreen.base.image="ghcr.io/gurucomputing/headscale-ui:2026.03.17"
LABEL evergreen.health.type="tcp"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.cap-drop="ALL"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
