# =============================================================================
# SOVEREIGN HARDENED SQLITE
# Generated from template - Version: 3.45.0
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=3.45.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends sqlite ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' sqlite 2>/dev/null || true
RUN mkdir -p /app /var/log/sqlite /var/cache/sqlite && chown -R sqlite:sqlite /app /var/log/sqlite /var/cache/sqlite 2>/dev/null || true
USER sqlite:sqlite
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD sqlite3 --version
ENTRYPOINT ["sqlite3"]
LABEL org.opencontainers.image.title="sqlite" \
      org.opencontainers.image.version="3.45.0" \
      org.opencontainers.image.vendor="SQLite" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
