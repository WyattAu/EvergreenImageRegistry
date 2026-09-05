ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM smallstep/step-ca:v0.30.2
USER 0
COPY --from=shim /shim /usr/local/bin/shim
USER 1000

ENV SHIM_METRICS_ENABLED="true"

EXPOSE 9000 9101
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \

  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9000"]

LABEL org.opencontainers.image.title="step-ca" evergreen.image.tier="standard" evergreen.constraint.nonroot="true"
LABEL evergreen.entrypoint.pattern="chainguard-repack" evergreen.security.cap-drop="ALL"
STOPSIGNAL SIGTERM
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="false"
LABEL evergreen.security.seccomp="runtime-default"
