# =============================================================================
# SOVEREIGN HARDENED OPENLDAP
# Generated from template - Version: 2.6.8
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.6.8
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends slapd ldap-utils ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' ldap 2>/dev/null || true
RUN mkdir -p /app /var/log/slapd /var/cache/slapd && chown -R ldap:ldap /app /var/log/slapd /var/cache/slapd 2>/dev/null || true
USER ldap
WORKDIR /app
EXPOSE 389 636
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ldapsearch -x -H ldap://localhost -b "" -s base "(objectclass=*)" 1.1
ENTRYPOINT ["slapd"]
LABEL org.opencontainers.image.title="openldap" \
      org.opencontainers.image.version="2.6.8" \
      org.opencontainers.image.vendor="OpenLDAP" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
