ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM mongo:7.0.12@sha256:ae1cf99fa7bfb007db8416ad4f3980c46054d949fa55d28e6d301a813fee6c06
COPY --from=shim /shim /usr/local/bin/shim

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
RUN mkdir -p /data/db && chown -R 65532:65532 /data/db
RUN mkdir -p /data/configdb && chown -R 65532:65532 /data/configdb
USER 65532:65532
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:27017"]

ENV SHIM_METRICS_ENABLED="true"

LABEL evergreen.entrypoint.pattern="repack-upstream-init"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 27017 9101
LABEL prometheus.io/scrape="true" prometheus.io/port="9101" prometheus.io/path="/metrics"
LABEL evergreen.image.tier="critical"
STOPSIGNAL SIGTERM
