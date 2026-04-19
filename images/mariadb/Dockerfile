# =============================================================================
# SOVEREIGN HARDENED MARIADB
# Generated from template - Version: 11.4
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=11.4
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends mariadb mariadb-client ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' mysql 2>/dev/null || true
RUN mkdir -p /app /var/log/mariadb /var/cache/mariadb && chown -R mysql:mysql /app /var/log/mariadb /var/cache/mariadb 2>/dev/null || true
USER mysql:mysql
WORKDIR /app
EXPOSE 3306
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD mariadb-admin ping
ENTRYPOINT ["mariadbd"]
LABEL org.opencontainers.image.title="mariadb" \
      org.opencontainers.image.version="11.4" \
      org.opencontainers.image.vendor="MariaDB" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
