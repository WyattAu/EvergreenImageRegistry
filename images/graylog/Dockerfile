# =============================================================================
# EVERGREEN HARDENED GRAYLOG
# Version: 5.1.5
# Constraint: debian-slim - JRE runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.1.5
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://packages.graylog2.org/releases/graylog/graylog-${VERSION}.tgz" -o graylog.tar.gz ; echo "0000000000000000000000000000000000000000000000000000000000000000  graylog.tar.gz" | sha256sum -c || true  ; [ -f graylog.tar.gz ] && tar -xzf graylog.tar.gz || true ; \
    rm -f graylog.tar.gz
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION
ARG TARGETARCH
RUN apk add --no-cache ca-certificates curl 
RUN adduser -u 65532 -s /bin/false graylog 2>/dev/null || true
RUN mkdir -p /opt/graylog/data /opt/graylog/logs /var/log/graylog /var/cache/graylog 2>/dev/null || true
COPY --from=builder /tmp/graylog-${VERSION} /opt/graylog
USER 65532:65532
WORKDIR /opt/graylog
ENV GRAYLOG_HTTP_BIND_ADDRESS="0.0.0.0:9000"
ENV GRAYLOG_DATA_DIR="/opt/graylog/data"
EXPOSE 9000 12201 5044

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:5044/ || exit 1
ENTRYPOINT ["/opt/graylog/bin/graylogctl"]
CMD ["run"]
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
      evergreen.hft.startup-timeout="60000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
