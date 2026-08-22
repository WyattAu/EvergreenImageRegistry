ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/valkey:9.0.4
USER 0
COPY --from=shim /shim /usr/local/bin/shim
USER 65532

ENV SHIM_METRICS_ENABLED="true"

EXPOSE 6379 9101
VOLUME /data

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:6379"]

LABEL org.opencontainers.image.title="valkey" evergreen.image.tier="critical" evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi" evergreen.entrypoint.pattern="chainguard-repack"
LABEL evergreen.security.cap-drop="ALL"
STOPSIGNAL SIGTERM
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="false"
LABEL evergreen.security.seccomp="runtime-default"
