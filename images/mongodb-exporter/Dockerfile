ARG SHIM_VERSION=v2.0.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim
FROM percona/mongodb_exporter:latest
COPY --from=shim /shim /usr/local/bin/shim
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \

  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9216"]
ENV SHIM_METRICS_ENABLED="true"
LABEL evergreen.entrypoint.pattern="repack-upstream-init" \
      evergreen.image.tier="standard" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true"
EXPOSE 9216 9101
STOPSIGNAL SIGTERM
