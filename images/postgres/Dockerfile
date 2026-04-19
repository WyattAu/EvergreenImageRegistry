# =============================================================================
# SOVEREIGN HARDENED POSTGRES
# Generated from template - Version: 17.4
# =============================================================================

ARG VERSION=17.4
ARG BUILD_DATE

FROM alpine:17.4-alpine
RUN apk add --no-cache postgresql17 postgresql17-client openssl ca-certificates ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id postgres 2>/dev/null || adduser -D -u 65534 postgres
RUN mkdir -p /app /var/log/postgres /var/cache/postgres && chown -R postgres:postgres /app /var/log/postgres /var/cache/postgres
USER postgres:postgres
WORKDIR /app
EXPOSE 5432
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD pg_isready -U postgres
ENTRYPOINT ["postgres"]
LABEL org.opencontainers.image.title="postgres" \
      org.opencontainers.image.version="17.4" \
      org.opencontainers.image.vendor="PostgreSQL" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
