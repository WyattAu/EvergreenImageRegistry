# =============================================================================
# SOVEREIGN HARDENED SQLITE
# Generated from template - Version: 3.45.0
# =============================================================================

ARG VERSION=3.45.0
ARG BUILD_DATE

FROM alpine:3.45.0-alpine
RUN apk add --no-cache sqlite ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id sqlite 2>/dev/null || adduser -D -u 65534 sqlite
RUN mkdir -p /app /var/log/sqlite /var/cache/sqlite && chown -R sqlite:sqlite /app /var/log/sqlite /var/cache/sqlite
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
      sovereign.constraint.nonroot="true"
