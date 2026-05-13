# =============================================================================
# EVERGREEN HARDENED OPENLDAP
# Generated from template - Version: 2.6.8
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.6.8
ARG BUILD_DATE

ARG TARGETARCH

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -D ldap 2>/dev/null || true && \
    mkdir -p /app /var/log/slapd /var/cache/slapd && chown -R ldap:ldap /app /var/log/slapd /var/cache/slapd 2>/dev/null || true
USER ldap
WORKDIR /app
EXPOSE 389 636

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:389/ || exit 1
ENTRYPOINT ["slapd"]
LABEL org.opencontainers.image.title="openldap" \
      org.opencontainers.image.description="openldap container image" \
      org.opencontainers.image.version="2.6.8" \
      org.opencontainers.image.vendor="OpenLDAP" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/openldap/openldap"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
