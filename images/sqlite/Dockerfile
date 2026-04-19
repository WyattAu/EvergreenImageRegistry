# =============================================================================
# SOVEREIGN HARDENED SQLITE
# Generated from template - Version: 3.45.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.45.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends sqlite3 ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' sqlite 2>/dev/null || true
RUN mkdir -p /app /var/log/sqlite3 /var/cache/sqlite3 && chown -R sqlite:sqlite /app /var/log/sqlite3 /var/cache/sqlite3 2>/dev/null || true
USER sqlite
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD sqlite3 --version
ENTRYPOINT ["sqlite3"]
LABEL org.opencontainers.image.title="sqlite" \
      org.opencontainers.image.version="3.45.1" \
      org.opencontainers.image.vendor="SQLite" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
