ARG SHIM_VERSION=v1.3.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM ghcr.io/frebib/zfs-exporter:latest
COPY --from=shim /shim /usr/local/bin/shim

HEALTHCHECK --interval=60s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9254"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/zfs-exporter"]
