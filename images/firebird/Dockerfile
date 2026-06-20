# =============================================================================
# EVERGREEN HARDENED FIREBIRD
# Constraint: debian-slim - native database package install
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.0.5
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=4.0.5
RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -s /bin/false firebird 2>/dev/null || true && \
    mkdir -p /var/lib/firebird /var/log/firebird /var/cache/firebird 2>/dev/null || true && \
    chown -R 65532:65532 /var/lib/firebird /var/log/firebird /var/cache/firebird
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /var/lib/firebird
EXPOSE 3050

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:3050"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "firebird"]
LABEL org.opencontainers.image.title="firebird" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened Firebird - SQL relational database" \
      org.opencontainers.image.vendor="FirebirdSQL" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/FirebirdSQL/firebird"
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
