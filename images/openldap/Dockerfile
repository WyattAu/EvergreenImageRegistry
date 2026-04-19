# =============================================================================
# SOVEREIGN HARDENED OPENLDAP
# Generated from template - Version: 2.6.8
# =============================================================================

ARG VERSION=2.6.8
ARG BUILD_DATE

FROM alpine:2.6.8-alpine
RUN apk add --no-cache openldap ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id ldap 2>/dev/null || adduser -D -u 65534 ldap
RUN mkdir -p /app /var/log/openldap /var/cache/openldap && chown -R ldap:ldap /app /var/log/openldap /var/cache/openldap
USER ldap:ldap
WORKDIR /app
EXPOSE 389 636
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ldapsearch
ENTRYPOINT ["slapd"]
LABEL org.opencontainers.image.title="openldap" \
      org.opencontainers.image.version="2.6.8" \
      org.opencontainers.image.vendor="OpenLDAP" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
