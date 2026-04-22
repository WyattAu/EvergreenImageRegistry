# =============================================================================
# SOVEREIGN HARDENED LDAP
# Generated from template - Version: 2.6.8
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.6.8
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apt-get update && apt-get install -y --no-install-recommends slapd ldap-utils ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65532 -g '' ldap 2>/dev/null || true
RUN mkdir -p /app /var/log/slapd /var/cache/slapd && chown -R ldap:ldap /app /var/log/slapd /var/cache/slapd 2>/dev/null || true
USER ldap
WORKDIR /app
EXPOSE 389 636
ENTRYPOINT ["slapd"]
LABEL org.opencontainers.image.title="ldap" \
      org.opencontainers.image.version="2.6.8" \
      org.opencontainers.image.vendor="OpenLDAP" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM