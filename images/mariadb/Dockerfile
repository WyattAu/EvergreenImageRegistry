# =============================================================================
# SOVEREIGN HARDENED MARIADB
# Generated from template - Version: 11.4.2
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=11.4.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN useradd -m -u 65534 -s /usr/sbin/nologin mysql 2>/dev/null || true
RUN mkdir -p /app /var/log/mariadbd /var/cache/mariadbd

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-server ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* && \
    apt-get purge -y --auto-remove apt apt-get dpkg 2>/dev/null || true
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /var/log/mariadbd /var/log/mariadbd
COPY --from=builder --chown=65534:65534 /var/cache/mariadbd /var/cache/mariadbd
USER 65534:65534
WORKDIR /app
EXPOSE 3306
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD mariadb-admin ping -h 127.0.0.1 --silent
ENTRYPOINT ["mariadbd"]
LABEL org.opencontainers.image.title="mariadb" \
      org.opencontainers.image.version="11.4.2" \
      org.opencontainers.image.vendor="MariaDB" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.constraint.hardened="true"
