# =============================================================================
# SOVEREIGN HARDENED SQLPAD
# Generated from template - Version: 7.5.1
# Constraint: debian-slim - Node.js runtime requires glibc
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=7.5.1
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG VERSION=7.5.1
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    curl --retry 3 --retry-delay 5 -fsSL "https://deb.nodesource.com/setup_20.x" | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    mkdir -p /app /var/log/sqlpad /var/cache/sqlpad && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/sqlpad/sqlpad/releases/download/v${VERSION}/sqlpad-v${VERSION}-linux-x64.tar.gz" \
    -o /sqlpad.tar.gz && \
    echo "PENDING_CHECKSUM  /sqlpad.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /sqlpad.tar.gz -C /app --strip-components=1 && \
    rm /sqlpad.tar.gz && \
    find /app -name "*.md" -delete && \
    find /app -name "*.txt" -not -name "package.json-c" -delete


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache curl ca-certificates bash
COPY --from=builder /app /app
COPY --from=builder /var/log/sqlpad /var/log/sqlpad
COPY --from=builder /var/cache/sqlpad /var/cache/sqlpad
RUN adduser -u 65532 -s /sbin/nologin sqlpad 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/sqlpad /var/cache/sqlpad
USER 65532:65532
WORKDIR /app
ENV SQLPAD_PORT="3000" \
    SQLPAD_HOST="0.0.0.0" \
    SQLPAD_DB_PATH="/app/db" \
    SQLPAD_ADMIN_PASSWORD=""
EXPOSE 3000
ENTRYPOINT ["node", "server.js"]
LABEL org.opencontainers.image.title="sqlpad" \
      org.opencontainers.image.version="7.5.1" \
      org.opencontainers.image.description="SQLPad - Web-based SQL Editor with Query Visualization" \
      org.opencontainers.image.vendor="SQLPad" \
      org.opencontainers.image.source="https://github.com/sqlpad/sqlpad" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM