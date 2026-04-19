# =============================================================================
# SOVEREIGN HARDENED OPENLDAP
# Generated from template - Version: 2.6.8
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=2.6.8
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends openldap ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' ldap 2>/dev/null || true
RUN mkdir -p /app /var/log/openldap /var/cache/openldap && chown -R ldap:ldap /app /var/log/openldap /var/cache/openldap 2>/dev/null || true
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
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
