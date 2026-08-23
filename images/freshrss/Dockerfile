ARG VERSION=1.29.0
ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM freshrss/freshrss:${VERSION}
COPY --from=shim /shim /usr/local/bin/shim
USER root

# Keep upstream entrypoint (FreshRSS uses its own startup scripts)
# Shim is only used for HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
USER 65532:65532
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENV SHIM_METRICS_ENABLED="true"

EXPOSE 9101
LABEL org.opencontainers.image.title="freshrss" \
      org.opencontainers.image.description="FreshRSS - self-hosted RSS feed reader (hardened with health-shim)" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="FreshRSS" \
      org.opencontainers.image.source="https://github.com/FreshRSS/FreshRSS" \
      evergreen.image.tier="2" \
      evergreen.constraint.hardened="true"
LABEL evergreen.base.image="upstream"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.entrypoint.pattern="repack-upstream-init"
STOPSIGNAL SIGTERM


