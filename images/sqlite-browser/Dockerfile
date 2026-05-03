# =============================================================================
# SOVEREIGN HARDENED SQLITE-BROWSER
# GUI-based SQLite database editor (DB Browser for SQLite)
# Constraint: debian-slim - requires Qt5 libs
# =============================================================================

ARG BUILD_DATE


FROM debian:bookworm-slim AS installer
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlitebrowser && \
    rm -rf /var/lib/apt/lists/* || true
RUN find /usr -type f -executable -name "sqlitebrowser" -exec strip --strip-all {} \; 2>/dev/null || true && \
    find /usr -type f -executable -name "sqlcipher" -exec strip --strip-all {} \; 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache sqlite-libs ca-certificates 
RUN mkdir -p /app /var/log/sqlite-browser 2>/dev/null || true
COPY --from=installer /usr/bin/sqlitebrowser /usr/local/bin/sqlitebrowser
RUN chown -R 65532:65532 /app /var/log/sqlite-browser
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/sqlitebrowser"]
LABEL org.opencontainers.image.title="sqlite-browser" \
      org.opencontainers.image.version="bookworm" \
      org.opencontainers.image.vendor="sqlitebrowser" \
      org.opencontainers.image.source="https://github.com/sqlitebrowser/sqlitebrowser" \
      org.opencontainers.image.description="GUI-based SQLite database editor" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
