# =============================================================================
# SOVEREIGN HARDENED COCKROACHDB
# Generated from template - Version: 23.2.0
# =============================================================================

ARG VERSION=23.2.0
ARG BUILD_DATE

FROM alpine:23.2.0-alpine
RUN apk add --no-cache cockroach ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id cockroach 2>/dev/null || adduser -D -u 65534 cockroach
RUN mkdir -p /app /var/log/cockroachdb /var/cache/cockroachdb && chown -R cockroach:cockroach /app /var/log/cockroachdb /var/cache/cockroachdb
USER cockroach:cockroach
WORKDIR /app
EXPOSE 26257 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD cockroach sql
ENTRYPOINT ["cockroach"]
LABEL org.opencontainers.image.title="cockroachdb" \
      org.opencontainers.image.version="23.2.0" \
      org.opencontainers.image.vendor="CockroachDB" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
