# =============================================================================
# EVERGREEN PLACEHOLDER - KDB+
# KDB+ Plus edition (proprietary, requires KX Systems license).
# Enhanced version with additional features over base KDB.
# =============================================================================


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates tzdata curl && \
    addgroup -S -g 65532 kdb 2>/dev/null || true && \
    adduser -u 65532 -G kdb -D -D -h /opt/kdb -s /bin/false kdb 2>/dev/null || true && \
    mkdir -p /opt/kdb/data /opt/kdb/logs /var/log/kdb ; \
    chown -R 65532:65532 /opt/kdb /var/log/kdb
USER 65532:65532
WORKDIR /opt/kdb
EXPOSE 5000
LABEL org.opencontainers.image.title="kdb-plus" \
      org.opencontainers.image.description="Placeholder for KX Systems KDB+ Plus edition. Requires license." \
      org.opencontainers.image.vendor="KX Systems" \
      evergreen.image.tier="2" \
      evergreen.image.category="database" \
      evergreen.image.note="KDB+ Plus is proprietary. Copy licensed q binary to /opt/kdb/q before use." \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/KxSystems/kdb" \
                  org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:5000/ || exit 1
