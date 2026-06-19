ARG VERSION=11.8
ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM mariadb:${VERSION}
COPY --from=shim /shim /usr/local/bin/shim

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:3306"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "docker-entrypoint.sh"]
CMD ["mariadbd"]

ENV SHIM_METRICS_ENABLED="true"

EXPOSE 9101
LABEL org.opencontainers.image.title="mariadb" \
      org.opencontainers.image.description="MariaDB - community-developed MySQL fork (hardened with health-shim)" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="MariaDB" \
      org.opencontainers.image.source="https://github.com/MariaDB/server" \
      evergreen.image.tier="critical" \
      evergreen.constraint.hardened="true"
LABEL evergreen.base.image="upstream"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGTERM
