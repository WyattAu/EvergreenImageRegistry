# =============================================================================
# EVERGREEN HARDENED FERRETDB
# Generated from template - Version: 2.7.0
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.7.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f70dc8d6a8b6a06824c92471a1a258030836b26b043881358b967bf73de7c5ab AS builder
ARG VERSION=2.7.0

RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/FerretDB/FerretDB/releases/download/v${VERSION}/ferretdb-amd64-linux -o /usr/local/bin/ferretdb && \
    echo "f81ecae6adf33e0c5e949acf85f94a40b0790c07b8f87d480b91518225da26b4  /usr/local/bin/ferretdb" | sha256sum -c ;  \
    chmod +x /usr/local/bin/ferretdb && strip --strip-all /usr/local/bin/ferretdb 2>/dev/null

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=2.7.0
COPY --from=builder /usr/local/bin/ferretdb /usr/local/bin/ferretdb
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
EXPOSE 27017 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:27017"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="ferretdb" \
      org.opencontainers.image.description="Evergreen hardened FerretDB - MongoDB-compatible database" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="FerretDB" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
            org.opencontainers.image.source="https://github.com/FerretDB/FerretDB"

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
