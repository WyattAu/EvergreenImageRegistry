ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM taigaio/taiga-protected:6.9.0@sha256:5f31fdb311431df45ceca4497abae05a312be9ca657564f20e164f825e9f1d5e
COPY --from=shim /shim /usr/local/bin/shim

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
USER 65532:65532
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8003"]


ENV SHIM_METRICS_ENABLED="true"

LABEL evergreen.entrypoint.pattern="repack-upstream-init"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 8003 9101
LABEL prometheus.io/scrape="true" prometheus.io/port="9101" prometheus.io/path="/metrics"
LABEL evergreen.image.tier="critical"
STOPSIGNAL SIGTERM
