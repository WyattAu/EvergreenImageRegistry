ARG TARGETARCH
# =============================================================================
# EVERGREEN HARDENED RQLITE
# Generated from template - Version: 8.10.0
# Constraint: scratch - static Go binary, purest form
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.10.0
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f70dc8d6a8b6a06824c92471a1a258030836b26b043881358b967bf73de7c5ab AS builder
ARG TARGETARCH
ARG VERSION=8.10.0
RUN mkdir -p /usr/local/bin/rqlited || true
RUN mkdir -p /usr/local/bin/rqlite && \
    mkdir -p /usr/local/bin/rqlited || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/rqlite/rqlite/releases/download/v${VERSION}/rqlite-v${VERSION}-linux-${TARGETARCH}.tar.gz -o /tmp/rqlite.tgz ; echo "fc3a01db82f24190e325adffd78b2fc9e2511451a356af33b4417db6a689554e  /tmp/rqlite.tgz" | sha256sum -c  ; [ -f /tmp/rqlite.tgz ] && tar -xzf /tmp/rqlite.tgz -C /tmp ; \
    strip --strip-all /tmp/rqlite-v${VERSION}-linux-${TARGETARCH}/rqlite 2>/dev/null && strip --strip-all /tmp/rqlite-v${VERSION}-linux-${TARGETARCH}/rqlited 2>/dev/null && \
    mv /tmp/rqlite-v${VERSION}-linux-${TARGETARCH}/rqlite /usr/local/bin/rqlite && mv /tmp/rqlite-v${VERSION}-linux-${TARGETARCH}/rqlited /usr/local/bin/rqlited && rm -rf /tmp/rqlite.tgz /tmp/rqlite-v${VERSION}-linux-${TARGETARCH} && \
    mkdir -p /usr/local/bin/rqlite /usr/local/bin/rqlited || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=8.10.0
COPY --from=builder /usr/local/bin/rqlite /usr/local/bin/rqlite
COPY --from=builder /usr/local/bin/rqlited /usr/local/bin/rqlited
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
EXPOSE 4001 4002

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:4001"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="rqlite" \
      org.opencontainers.image.description="Evergreen hardened rqlite - distributed SQLite database" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="rqlite" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
            org.opencontainers.image.source="https://github.com/rqlite/rqlite"

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
