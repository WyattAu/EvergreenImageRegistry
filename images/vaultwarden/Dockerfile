ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM vaultwarden/server:1.36.0@sha256:d626d04934cd1192ad8ced1adb975099fca78cec33ab467d2d3c923cde7f3b0c
USER 0
COPY --from=shim /shim /usr/local/bin/shim
USER 65532:65532

ENV SHIM_METRICS_ENABLED="true" ROCKET_ADDRESS=0.0.0.0 ROCKET_PORT=80

EXPOSE 80 9101
VOLUME /data

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

LABEL org.opencontainers.image.title="vaultwarden" evergreen.image.tier="critical" evergreen.constraint.nonroot="true"
LABEL evergreen.entrypoint.pattern="repack-upstream-init" evergreen.security.cap-drop="ALL"
STOPSIGNAL SIGTERM
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="false"
LABEL evergreen.security.seccomp="runtime-default"
