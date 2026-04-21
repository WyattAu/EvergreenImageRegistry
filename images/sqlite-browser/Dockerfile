# =============================================================================
# SOVEREIGN HARDENED SQLITE-BROWSER
# GUI-based SQLite database editor (DB Browser for SQLite)
# Constraint: debian-slim - requires Qt5 libs
# =============================================================================

ARG BUILD_DATE

FROM debian:bookworm-slim AS installer
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlitebrowser && \
    rm -rf /var/lib/apt/lists/*
RUN find /usr -type f -executable -name "sqlitebrowser" -exec strip --strip-all {} \; 2>/dev/null || true && \
    find /usr -type f -executable -name "sqlcipher" -exec strip --strip-all {} \; 2>/dev/null || true

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libqt5core5t64 libqt5gui5t64 libqt5widgets5t64 libqt5network5t64 \
    libqt5svg5 libsqlcipher0 libsqlite3-0 libssl3 \
    libqscintilla2-qt5-15 ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/sqlite-browser
COPY --from=installer /usr/bin/sqlitebrowser /usr/local/bin/sqlitebrowser
RUN chown -R 65534:65534 /app /var/log/sqlite-browser
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/usr/local/bin/sqlitebrowser", "--version"]
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
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
