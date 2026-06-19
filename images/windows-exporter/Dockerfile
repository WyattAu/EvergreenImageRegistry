# STUB: windows-exporter is Windows-only, no Linux binary exists.
# This image exists for registry completeness only.
# Uses shim to keep container alive (health server) on Linux.
ARG VERSION=0.25.0
ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim

ARG VERSION=0.25.0
USER 65532:65532
WORKDIR /tmp
EXPOSE 9182 9101

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL evergreen.entrypoint.pattern="repack-upstream-init"
LABEL org.opencontainers.image.title="windows-exporter" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="prometheus-community" \
      org.opencontainers.image.source="https://github.com/prometheus-community/windows_exporter" \
      org.opencontainers.image.description="Prometheus exporter for Windows metrics (Windows-only, stub on Linux — use prometheus-node-exporter)" \
      evergreen.image.tier="standard" \
      evergreen.image.category="monitoring" \
      evergreen.image.status="stub" \
      evergreen.constraint.nonroot="true"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
