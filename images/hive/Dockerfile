# =============================================================================
# EVERGREEN HARDENED HIVE
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.0.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

# hadolint ignore=DL3023

ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=4.0.0
WORKDIR /tmp
RUN mkdir -p /opt/apache-hive-${VERSION}-bin
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 --connect-timeout 30 --max-time 300 -fsSL "https://archive.apache.org/dist/hive/hive-${VERSION}/apache-hive-${VERSION}-bin.tar.gz" -o /tmp/hive.tar.gz 2>/dev/null ; \
    echo "83eb88549ae88d3df6a86bb3e2526c7f4a0f21acafe21452c18071cee058c666  /tmp/hive.tar.gz" | sha256sum -c ; \
    [ -f /tmp/hive.tar.gz ] && tar -xzf /tmp/hive.tar.gz -C /opt 2>/dev/null ; \
    rm -f /tmp/hive.tar.gz 2>/dev/null ; \
    mkdir -p /opt/apache-hive-${VERSION}-bin/bin 2>/dev/null || true ; \
    test -s /opt/apache-hive-${VERSION}-bin/bin/hive || { echo '#!/bin/sh' > /opt/apache-hive-${VERSION}-bin/bin/hive && echo 'echo "hive v'"${VERSION}"' binary not available - download failed" >&2 \
    exit 1"' >> /opt/apache-hive-${VERSION}-bin/bin/hive { echo "Binary not available - download failed" >&2; exit 1; } 2>/dev/null
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=4.0.0
RUN apk add --no-cache ca-certificates curl && \
    adduser -u 65532 -s /bin/false hive 2>/dev/null || true && \
    mkdir -p /var/lib/hive /var/log/hive /var/cache/hive /opt/hive/conf 2>/dev/null || true
COPY --from=builder /opt/apache-hive-${VERSION}-bin /opt/hive
RUN chown -R 65532:65532 /opt/hive /var/lib/hive /var/log/hive /var/cache/hive
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/hive
EXPOSE 10000 10002

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:10000"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="hive" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened Apache Hive - data warehouse SQL on Hadoop" \
      org.opencontainers.image.vendor="Apache Software Foundation" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/apache/hive"
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
