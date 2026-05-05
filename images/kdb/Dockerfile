# =============================================================================
# EVERGREEN PLACEHOLDER - KDB
# KDB+ is a proprietary in-memory columnar database by KX Systems.
# No public binaries or container images are available.
# =============================================================================


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates tzdata curl && \
    addgroup -S -g 65532 kdb 2>/dev/null || true && \
    adduser -u 65532 -G kdb -D -D -h /opt/kdb -s /bin/false kdb 2>/dev/null || true && \
    mkdir -p /opt/kdb/data /opt/kdb/logs /var/log/kdb ; \
    chown -R 65532:65532 /opt/kdb /var/log/kdb
USER 65532:65532
WORKDIR /opt/kdb
EXPOSE 5000
LABEL org.opencontainers.image.title="kdb" \
      org.opencontainers.image.description="Placeholder for KX Systems KDB+ proprietary database. Requires license." \
      org.opencontainers.image.vendor="KX Systems" \
      evergreen.image.tier="2" \
      evergreen.image.category="database" \
      evergreen.image.note="KDB+ is proprietary. Copy licensed q binary to /opt/kdb/q before use." \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/kdb-software/kdb" \
                  org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:5000/ || exit 1
