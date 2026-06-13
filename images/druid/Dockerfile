ARG VERSION=37.0.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM apache/druid:${VERSION} AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=37.0.0
RUN apk add --no-cache ca-certificates python3 && \
    adduser -D -u 65532 -s /bin/false druid 2>/dev/null || true && \
    mkdir -p /var/lib/druid /var/log/druid /var/cache/druid /opt 2>/dev/null || true
COPY --from=upstream /opt/druid /opt/druid
RUN chown -R druid:druid /opt/druid /var/lib/druid /var/log/druid /var/cache/druid 2>/dev/null || true

WORKDIR /opt/druid

EXPOSE 8088 8888 8280
EXPOSE 9101

LABEL org.opencontainers.image.title="druid" org.opencontainers.image.version="29.0.1" org.opencontainers.image.vendor="Apache" org.opencontainers.image.description="Evergreen hardened Apache Druid - real-time analytics database" evergreen.image.tier="1" evergreen.image.category="database" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.base.image="wolfi" \
      org.opencontainers.image.source="https://github.com/apache/druid"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8088"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
