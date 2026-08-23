ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM ghcr.io/dexidp/dex:v2.45.1
USER 0
COPY --from=shim /shim /usr/local/bin/shim
USER 1001

ENV SHIM_METRICS_ENABLED="true"

EXPOSE 5556 9101
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
USER 65532:65532
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:5556"]

LABEL org.opencontainers.image.title="dex" evergreen.image.tier="critical" evergreen.constraint.nonroot="true"
LABEL evergreen.entrypoint.pattern="chainguard-repack" evergreen.security.cap-drop="ALL"
STOPSIGNAL SIGTERM
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="false"
LABEL evergreen.security.seccomp="runtime-default"
