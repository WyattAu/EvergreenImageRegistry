ARG VERSION=1.152.1
ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM matrixdotorg/synapse:latest
COPY --from=shim /shim /usr/local/bin/shim

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8008"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/python3"]
CMD ["-m", "synapse.app.homeserver", "--config-path", "/data/homeserver.yaml"]

ENV SHIM_METRICS_ENABLED="true"

EXPOSE 9101
LABEL org.opencontainers.image.title="synapse" \
      org.opencontainers.image.description="Synapse - Matrix homeserver (hardened with health-shim)" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Matrix.org Foundation" \
      org.opencontainers.image.source="https://github.com/element-hq/synapse" \
      evergreen.image.tier="standard" \
      evergreen.constraint.hardened="true"
LABEL evergreen.base.image="upstream"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGTERM
