# =============================================================================
# EVERGREEN HARDENED ZFS EXPORTER
# Repacked from ghcr.io/frebib/zfs-exporter (actively maintained)
# Replaces dead fberning/zfs-exporter upstream
# =============================================================================
# NOTE: Metrics differ from previous fberning version.
# Update dashboards/alerts for new metric names and port 9254 (was 9134).
#
# zfs-exporter is dynamically linked to libzfs, ld-musl, and 16 other .so files.
# Must copy all shared libraries from the upstream Alpine image into scratch.

ARG VERSION=0.0.12
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM ghcr.io/frebib/zfs-exporter:0.0.12 AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=upstream /usr/bin/zfs-exporter /zfs-exporter
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=upstream /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
# All transitive shared library dependencies (libzfs, libcrypto, libkrb5, etc.)
COPY --from=upstream /usr/lib/libzfs.so.6 /usr/lib/libzfs.so.6
COPY --from=upstream /usr/lib/libnvpair.so.3 /usr/lib/libnvpair.so.3
COPY --from=upstream /usr/lib/libzfs_core.so.3 /usr/lib/libzfs_core.so.3
COPY --from=upstream /usr/lib/libuutil.so.3 /usr/lib/libuutil.so.3
COPY --from=upstream /usr/lib/libuuid.so.1 /usr/lib/libuuid.so.1
COPY --from=upstream /usr/lib/libblkid.so.1 /usr/lib/libblkid.so.1
COPY --from=upstream /usr/lib/libcrypto.so.3 /usr/lib/libcrypto.so.3
COPY --from=upstream /usr/lib/libz.so.1 /usr/lib/libz.so.1
COPY --from=upstream /usr/lib/libintl.so.8 /usr/lib/libintl.so.8
COPY --from=upstream /usr/lib/libtirpc.so.3 /usr/lib/libtirpc.so.3
COPY --from=upstream /usr/lib/libeconf.so.0 /usr/lib/libeconf.so.0
COPY --from=upstream /usr/lib/libgssapi_krb5.so.2 /usr/lib/libgssapi_krb5.so.2
COPY --from=upstream /usr/lib/libkrb5.so.3 /usr/lib/libkrb5.so.3
COPY --from=upstream /usr/lib/libk5crypto.so.3 /usr/lib/libk5crypto.so.3
COPY --from=upstream /usr/lib/libcom_err.so.2 /usr/lib/libcom_err.so.2
COPY --from=upstream /usr/lib/libkrb5support.so.0 /usr/lib/libkrb5support.so.0
COPY --from=upstream /usr/lib/libkeyutils.so.1 /usr/lib/libkeyutils.so.1

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 9254

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9254"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="zfs-exporter" \
      org.opencontainers.image.description="ZFS Exporter - Prometheus exporter for ZFS pool and dataset metrics" \
      org.opencontainers.image.version="0.0.12" \
      org.opencontainers.image.vendor="frebib" \
      org.opencontainers.image.source="https://github.com/frebib/zfs-exporter" \
      evergreen.image.tier="3" \
      evergreen.image.category="monitoring" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.image.note="Switched from dead fberning/zfs-exporter to frebib/zfs-exporter. Metrics and port changed (9134->9254). Update dashboards. Fixed: added all shared lib dependencies." \
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
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
