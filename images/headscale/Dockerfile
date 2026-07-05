# Evergreen hardened headscale
# Repack of upstream headscale/headscale with health-shim overlay
# Note: headscale base is distroless (ko-built, no /bin/sh) — no RUN commands possible
ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM headscale/headscale:v0.29.2

COPY --from=shim /shim /usr/local/bin/shim

USER 65532:65532

ENV SHIM_METRICS_ENABLED="true"
EXPOSE 8080 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/ko-app/headscale serve"]

LABEL org.opencontainers.image.title="headscale" \
      org.opencontainers.image.description="Headscale - open source Tailscale control server" \
      org.opencontainers.image.version="0.29.2" \
      org.opencontainers.image.vendor="Juan Font" \
      org.opencontainers.image.source="https://github.com/juanfont/headscale" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="headscale/headscale:v0.29.2"
LABEL evergreen.health.type="tcp"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.security.read-only-rootfs="true"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
