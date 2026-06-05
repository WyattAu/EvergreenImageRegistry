ARG TARGETARCH
# =============================================================================
# EVERGREEN HARDENED CRDB-INIT
# Generated from template - Version: 23.2.3
# Constraint: scratch - static Go binary (cockroachdb init entrypoint)
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=23.2.3
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f70dc8d6a8b6a06824c92471a1a258030836b26b043881358b967bf73de7c5ab AS builder
ARG TARGETARCH
ARG VERSION=23.2.3
RUN mkdir -p /usr/local/bin/cockroach || true
RUN apt-get update 2>/dev/null && apt-get install -y --no-install-recommends binutils curl ca-certificates 2>/dev/null && rm -rf /var/lib/apt/lists/* 2>/dev/null && \
    curl --retry 3 --retry-delay 5 -fsSL "https://binaries.cockroachdb.com/cockroach-v${VERSION}.linux-${TARGETARCH}.tgz" -o /tmp/cockroach.tgz 2>/dev/null ; \
    [ -f /tmp/cockroach.tgz ] && tar -xzf /tmp/cockroach.tgz -C /tmp 2>/dev/null ; \
    strip --strip-all /tmp/cockroach-v${VERSION}.linux-${TARGETARCH}/cockroach 2>/dev/null ; \
    mv /tmp/cockroach-v${VERSION}.linux-${TARGETARCH}/cockroach /usr/local/bin/cockroach 2>/dev/null && \
    rm -rf /tmp/cockroach.tgz /tmp/cockroach-v${VERSION}.linux-${TARGETARCH} 2>/dev/null || true && { echo "Binary not available - download failed" >&2; exit 1; }
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=23.2.3
COPY --from=builder /usr/local/bin/cockroach /usr/local/bin/cockroach
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 26257

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:26257"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="crdb-init" \
      org.opencontainers.image.description="Evergreen hardened CockroachDB init entrypoint" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Cockroach Labs" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
            org.opencontainers.image.source="https://github.com/cockroachdb/cockroach"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
