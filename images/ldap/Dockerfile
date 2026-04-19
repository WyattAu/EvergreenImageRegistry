# =============================================================================
# SOVEREIGN HARDENED LDAP
# Generated from template - Version: 2.6.8
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=2.6.8
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:2.6.8
RUN apk add --no-cache openldap ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 ldap 2>/dev/null || true
RUN mkdir -p /app /var/log/ldap /var/cache/ldap && chown -R ldap:ldap /app /var/log/ldap /var/cache/ldap 2>/dev/null || true
USER ldap:ldap
WORKDIR /app
EXPOSE 389 636
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ldapsearch
ENTRYPOINT ["slapd"]
LABEL org.opencontainers.image.title="ldap" \
      org.opencontainers.image.version="2.6.8" \
      org.opencontainers.image.vendor="OpenLDAP" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
