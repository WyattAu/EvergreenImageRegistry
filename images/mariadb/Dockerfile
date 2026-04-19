# =============================================================================
# SOVEREIGN HARDENED MARIADB
# Generated from template - Version: 11.4.2
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=11.4.2
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends default-mysql-server ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' mysql 2>/dev/null || true
RUN mkdir -p /app /var/log/mariadbd /var/cache/mariadbd && chown -R mysql:mysql /app /var/log/mariadbd /var/cache/mariadbd 2>/dev/null || true
USER mysql
WORKDIR /app
EXPOSE 3306
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD mariadbd mariadb-admin ping
ENTRYPOINT ["mariadbd"]
LABEL org.opencontainers.image.title="mariadb" \
      org.opencontainers.image.version="11.4.2" \
      org.opencontainers.image.vendor="MariaDB" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
