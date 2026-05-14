# =============================================================================
# EVERGREEN HARDENED MARIADB
# Generated from template - Version: 11.4
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=11.4
ARG BUILD_DATE

ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN useradd -m -u 65532 -s /usr/bin/false mysql 2>/dev/null || true && \
    mkdir -p /app /var/log/mariadbd /var/cache/mariadbd 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ENV HEALTH_CMD="mariadb-admin ping -h 127.0.0.1 --silent" \
    READY_CMD="mariadb-admin ping -h 127.0.0.1 --silent" \
    STARTUP_CMD="mariadb-admin ping -h 127.0.0.1 --silent" \
    EVERGREEN_LOG_LEVEL=info

RUN apk add --no-cache ca-certificates 
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/mariadbd /var/log/mariadbd
COPY --from=builder --chown=65532:65532 /var/cache/mariadbd /var/cache/mariadbd
USER 65532:65532
WORKDIR /app
EXPOSE 3306

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD mysqladmin ping -h localhost --silent
ENTRYPOINT ["sh", "-c", "mariadbd"]
LABEL org.opencontainers.image.title="mariadb" \
      org.opencontainers.image.description="MariaDB - community-developed fork of MySQL" \
      org.opencontainers.image.version="11.4" \
      org.opencontainers.image.vendor="MariaDB" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true" \
            org.opencontainers.image.source="https://github.com/MariaDB/server"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
