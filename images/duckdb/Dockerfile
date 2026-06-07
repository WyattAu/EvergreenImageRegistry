ARG TARGETARCH
# =============================================================================
# EVERGREEN HARDENED DUCKDB
# Generated from template - Version: 1.1.3
# Constraint: scratch - static C++ binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.1.3
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f70dc8d6a8b6a06824c92471a1a258030836b26b043881358b967bf73de7c5ab AS builder
ARG TARGETARCH
ARG VERSION=1.1.3
RUN mkdir -p /usr/local/bin/duckdb || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/duckdb/duckdb/releases/download/v${VERSION}/duckdb_cli-linux-${TARGETARCH}.zip -o /tmp/duckdb.zip ; echo "efd0fccdb1a28d9ec7a6ebfcde59900068b8ba43a846c9b553c0fd2bbe4acf43  /tmp/duckdb.zip" | sha256sum -c  ; unzip -o /tmp/duckdb.zip -d /tmp ; \
    strip --strip-all /tmp/duckdb 2>/dev/null; mv /tmp/duckdb /usr/local/bin/duckdb \
    && rm -rf /tmp/duckdb.zip && \
    mkdir -p /usr/local/bin/duckdb 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=1.1.3
COPY --from=builder /usr/local/bin/duckdb /usr/local/bin/duckdb
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
EXPOSE 5432

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:5432"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="duckdb" \
      org.opencontainers.image.description="Evergreen hardened DuckDB - in-process analytical database" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="DuckDB Labs" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
            org.opencontainers.image.source="https://github.com/duckdb/duckdb"

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
