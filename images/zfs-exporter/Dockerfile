# =============================================================================
# EVERGREEN HARDENED ZFS EXPORTER
# Repacked from ghcr.io/frebib/zfs-exporter ( actively maintained)
# Replaces dead fberning/zfs-exporter upstream
# =============================================================================
# NOTE: Metrics differ from previous fberning version.
# Update dashboards/alerts for new metric names and port 9254 (was 9134).

ARG VERSION=latest
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM ghcr.io/frebib/zfs-exporter:latest AS upstream

FROM scratch
COPY --from=upstream /usr/bin/zfs-exporter /zfs-exporter
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
WORKDIR /app
EXPOSE 9254

HEALTHCHECK NONE
ENTRYPOINT ["/zfs-exporter"]
LABEL org.opencontainers.image.title="zfs-exporter" \
      org.opencontainers.image.description="ZFS Exporter - Prometheus exporter for ZFS pool and dataset metrics" \
      org.opencontainers.image.version="latest" \
      org.opencontainers.image.vendor="frebib" \
      org.opencontainers.image.source="https://github.com/frebib/zfs-exporter" \
      evergreen.image.tier="3" \
      evergreen.image.category="monitoring" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.image.note="Switched from dead fberning/zfs-exporter to frebib/zfs-exporter. Metrics and port changed (9134->9254). Update dashboards." \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
