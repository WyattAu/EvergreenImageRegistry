# =============================================================================
# SOVEREIGN HARDENED COCKROACHDB
# Generated from template - Version: 23.2.0
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=23.2.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:23.2.0
RUN apk add --no-cache cockroach ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 cockroach 2>/dev/null || true
RUN mkdir -p /app /var/log/cockroachdb /var/cache/cockroachdb && chown -R cockroach:cockroach /app /var/log/cockroachdb /var/cache/cockroachdb 2>/dev/null || true
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
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
