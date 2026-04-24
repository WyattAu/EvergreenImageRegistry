# =============================================================================
# SOVEREIGN PLACEHOLDER - KDB+
# KDB+ Plus edition (proprietary, requires KX Systems license).
# Enhanced version with additional features over base KDB.
# =============================================================================


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates tzdata curl

RUN addgroup -S 65532 -r kdb 2>/dev/null || true && \
    adduser -u 65532 -G kdb -D -D -h /opt/kdb -s /sbin/nologin kdb 2>/dev/null || true && \
    mkdir -p /opt/kdb/data /opt/kdb/logs /var/log/kdb && \
    chown -R 65532:65532 /opt/kdb /var/log/kdb
USER 65532:65532
WORKDIR /opt/kdb
EXPOSE 5000
LABEL org.opencontainers.image.title="kdb-plus" \
      org.opencontainers.image.description="Placeholder for KX Systems KDB+ Plus edition. Requires license." \
      org.opencontainers.image.vendor="KX Systems" \
      sovereign.image.tier="2" \
      sovereign.image.category="database" \
      sovereign.image.note="KDB+ Plus is proprietary. Copy licensed q binary to /opt/kdb/q before use." \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
