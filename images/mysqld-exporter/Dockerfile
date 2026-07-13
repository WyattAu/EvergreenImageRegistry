ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM prom/mysqld-exporter:v0.19.0
COPY --from=shim /shim /usr/local/bin/shim

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9104"]

LABEL evergreen.image.tier="standard"
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/bin/mysqld_exporter"]
USER 65532:65532
STOPSIGNAL SIGTERM
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
EXPOSE 8080 9101
LABEL evergreen.security.read-only-rootfs="false"
LABEL evergreen.security.seccomp="runtime-default"
