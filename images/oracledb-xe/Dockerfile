ARG VERSION=21.3.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM gvenzl/oracle-xe:21-slim@sha256:523f7afc7a05b1ddd4420d4de72f96024c58545d5946202b42d6d616c3c4b475 AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=21.3.0
RUN apk add --no-cache bc ca-certificates wget netcat-openbsd && \
    adduser -D -u 65532 -s /bin/false oracle 2>/dev/null || true && \
    mkdir -p /var/lib/oracle /var/log/oracle /var/cache/oracle /opt/oracle 2>/dev/null || true
COPY --from=upstream /opt/oracle /opt/oracle
RUN mkdir -p /etc/oracle || true
COPY --from=upstream /etc/oracle /etc/oracle
RUN chown -R 65532:65532 /opt/oracle /var/lib/oracle /var/log/oracle /var/cache/oracle 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/oracle
EXPOSE 1521 5500

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:1521"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="oracledb-xe" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened Oracle DB XE - extracted from gvenzl/oracle-xe" \
      org.opencontainers.image.vendor="Oracle" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.image.note="Extracted from gvenzl/oracle-xe@sha256:ecdf4302ac3d134e1bac5ef6e0c223c2d0f4d4d2b6d551aa79b2346f1ab8f792 community image. Oracle license applies." \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/oracle/docker-images"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
