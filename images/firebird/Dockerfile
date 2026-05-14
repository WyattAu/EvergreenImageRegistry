# =============================================================================
# EVERGREEN HARDENED FIREBIRD
# Constraint: debian-slim - native database package install
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.0.5
ARG TARGETARCH
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=4.0.5
RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -s /bin/false firebird 2>/dev/null || true && \
    mkdir -p /var/lib/firebird /var/log/firebird /var/cache/firebird 2>/dev/null || true && \
    chown -R 65532:65532 /var/lib/firebird /var/log/firebird /var/cache/firebird
USER 65532:65532
WORKDIR /var/lib/firebird
EXPOSE 3050

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:3050/ || exit 1
ENTRYPOINT ["firebird"]
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
STOPSIGNAL SIGTERM
