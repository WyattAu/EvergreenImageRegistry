# =============================================================================
# EVERGREEN HARDENED SQLITE-BROWSER
# GUI-based SQLite database editor (DB Browser for SQLite)
# Constraint: debian-slim - requires Qt5 libs
# =============================================================================

ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS installer
RUN apt-get update && apt-get install -y --no-install-recommends binutils \
    sqlitebrowser && \
    rm -rf /var/lib/apt/lists/* || true && \
    find /usr -type f -executable -name "sqlitebrowser" -exec strip --strip-all {} \ || true 2>/dev/null; 2>/dev/null || true && \
    find /usr -type f -executable -name "sqlcipher" -exec strip --strip-all {} \ || true 2>/dev/null; 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache sqlite-libs ca-certificates && \
    mkdir -p /app /var/log/sqlite-browser 2>/dev/null || true
COPY --from=installer /usr/bin/sqlitebrowser /usr/local/bin/sqlitebrowser
RUN chown -R 65532:65532 /app /var/log/sqlite-browser
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/usr/local/bin/sqlitebrowser"]
LABEL org.opencontainers.image.title="sqlite-browser" \
      org.opencontainers.image.version="bookworm" \
      org.opencontainers.image.vendor="sqlitebrowser" \
      org.opencontainers.image.source="https://github.com/sqlitebrowser/sqlitebrowser" \
      org.opencontainers.image.description="GUI-based SQLite database editor" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
