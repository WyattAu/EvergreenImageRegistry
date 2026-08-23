ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM hashicorp/vault:1.18.1@sha256:3580fa352195aa7e76449cb8fadeef6d2f90a454c38982d30cf094e9013be786
COPY --from=shim /shim /usr/local/bin/shim

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
RUN mkdir -p /vault/file && chown -R 65532:65532 /vault/file
RUN mkdir -p /vault/config && chown -R 65532:65532 /vault/config
USER 65532:65532
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8200"]

ENV SHIM_METRICS_ENABLED="true"

LABEL evergreen.entrypoint.pattern="repack-upstream-init"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 8200 9101
LABEL prometheus.io/scrape="true" prometheus.io/port="9101" prometheus.io/path="/metrics"
LABEL evergreen.image.tier="critical"
STOPSIGNAL SIGTERM
