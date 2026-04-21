# =============================================================================
# SOVEREIGN HARDENED SQLPAD
# Generated from template - Version: 7.5.1
# Constraint: debian-slim - Node.js runtime requires glibc
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=7.5.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    curl -fsSL "https://deb.nodesource.com/setup_20.x" | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    mkdir -p /app /var/log/sqlpad /var/cache/sqlpad && \
    curl -fsSL "https://github.com/sqlpad/sqlpad/releases/download/v${VERSION}/sqlpad-v${VERSION}-linux-x64.tar.gz" \
    -o /sqlpad.tar.gz && \
    echo "PENDING_CHECKSUM  /sqlpad.tar.gz" | sha256sum -c - && \
    tar -xzf /sqlpad.tar.gz -C /app --strip-components=1 && \
    rm /sqlpad.tar.gz && \
    find /app -name "*.md" -delete && \
    find /app -name "*.txt" -not -name "package.json" -delete

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    curl -fsSL "https://deb.nodesource.com/setup_20.x" | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder /app /app
COPY --from=builder /var/log/sqlpad /var/log/sqlpad
COPY --from=builder /var/cache/sqlpad /var/cache/sqlpad
RUN useradd -m -u 65534 -s /usr/sbin/nologin sqlpad 2>/dev/null || true && \
    chown -R 65534:65534 /app /var/log/sqlpad /var/cache/sqlpad
USER 65534:65534
WORKDIR /app
ENV SQLPAD_PORT="3000" \
    SQLPAD_HOST="0.0.0.0" \
    SQLPAD_DB_PATH="/app/db" \
    SQLPAD_ADMIN_PASSWORD=""
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["curl", "-f", "http://localhost:3000/api/app"]
ENTRYPOINT ["node", "server.js"]
LABEL org.opencontainers.image.title="sqlpad" \
      org.opencontainers.image.version="7.5.1" \
      org.opencontainers.image.description="SQLPad - Web-based SQL Editor with Query Visualization" \
      org.opencontainers.image.vendor="SQLPad" \
      org.opencontainers.image.source="https://github.com/sqlpad/sqlpad" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
