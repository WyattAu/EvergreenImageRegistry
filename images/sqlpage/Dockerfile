# =============================================================================
# EVERGREEN HARDENED SQLPAGE
# SQL-only web application framework
# https://github.com/sqlpage/SQLPage
# =============================================================================

ARG VERSION=0.43.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder
ARG VERSION=0.43.0

RUN apk add --no-cache ca-certificates curl && \
    curl --retry 3 --retry-delay 5 -fSL "https://github.com/sqlpage/SQLPage/releases/download/v${VERSION}/sqlpage-linux.tgz" -o /tmp/sqlpage.tgz \
    && echo "136c3f9b56448304d4f6dc85dd279a67c49ca32c16deb2a3c38f35519c2626f3  /tmp/sqlpage.tgz" | sha256sum -c
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=0.43.0
ARG BUILD_DATE
RUN apk add --no-cache ca-certificates tzdata libgcc
COPY --from=builder /tmp/sqlpage.tgz /tmp/sqlpage.tgz
RUN addgroup -S -g 65532 sqlpage 2>/dev/null || true && \
    adduser -u 65532 -G sqlpage -D -h /opt/sqlpage -s /bin/false sqlpage 2>/dev/null || true && \
    mkdir -p /opt/sqlpage /var/lib/sqlpage && \
    cd /opt/sqlpage && tar xzf /tmp/sqlpage.tgz && rm -f /tmp/sqlpage.tgz && \
    chown -R 65532:65532 /opt/sqlpage /var/lib/sqlpage

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/sqlpage
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="sqlpage" \
      org.opencontainers.image.description="SQL-only web application framework" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.source="https://github.com/sqlpage/SQLPage" \
      evergreen.image.tier="1" \
      evergreen.image.category="web" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="prometheus"
LABEL evergreen.health.type="http"
LABEL evergreen.health.path="/"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
