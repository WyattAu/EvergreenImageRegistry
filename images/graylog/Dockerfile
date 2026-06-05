# =============================================================================
# EVERGREEN HARDENED GRAYLOG
# Version: 5.1.5
# Constraint: debian-slim - JRE runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.1.5
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=5.1.5
WORKDIR /tmp
RUN mkdir -p /tmp/graylog-${VERSION}
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://packages.graylog2.org/releases/graylog/graylog-${VERSION}.tgz" -o graylog.tar.gz ; echo "79a42544faa9855b25ba71350c61480fa0c300696726f3ee15a1c378d55189e2  graylog.tar.gz" | sha256sum -c  ; [ -f graylog.tar.gz ] && tar -xzf graylog.tar.gz ; \
    rm -f graylog.tar.gz
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=5.1.5
RUN apk add --no-cache ca-certificates curl && \
    adduser -u 65532 -s /bin/false graylog 2>/dev/null || true && \
    mkdir -p /opt/graylog/data /opt/graylog/logs /var/log/graylog /var/cache/graylog 2>/dev/null || true
COPY --from=builder /tmp/graylog-${VERSION} /opt/graylog
USER 65532:65532
WORKDIR /opt/graylog
ENV GRAYLOG_HTTP_BIND_ADDRESS="0.0.0.0:9000"
ENV GRAYLOG_DATA_DIR="/opt/graylog/data"
EXPOSE 9000 12201 5044

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:5044"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/opt/graylog/bin/graylogctl", "--", "run"]
LABEL org.opencontainers.image.title="graylog" \
      org.opencontainers.image.description="Evergreen hardened Graylog - centralized log management platform" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Graylog" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="observability" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="15s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="60000ms" \
            org.opencontainers.image.source="https://github.com/Graylog2/graylog2-server"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
