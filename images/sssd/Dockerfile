# =============================================================================
# EVERGREEN HARDENED SSSD
# System Security Services Daemon (LDAP/Kerberos authentication)
# Constraint: debian-slim hardened
# =============================================================================


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates tzdata && \
    mkdir -p /var/lib/sss /var/log/sssd /etc/sssd ; \
    chown -R root:root /var/lib/sss /var/log/sssd /etc/sssd && \
    chmod 700 /var/lib/sss /var/log/sssd /etc/sssd
EXPOSE 0
LABEL org.opencontainers.image.title="sssd" \
      org.opencontainers.image.description="Evergreen SSSD - System Security Services Daemon for LDAP/Kerberos auth" \
      evergreen.image.tier="2" \
      evergreen.image.status="functional" \
      evergreen.image.category="auth" \
      evergreen.image.note="SSSD requires privileged mode for PAM/NSS integration. Runs as root for PAM module access." \
            org.opencontainers.image.source="https://github.com/SSSD/sssd" \
                  org.opencontainers.image.version="unknown"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:0/ || exit 1
CMD ["/bin/sh"]
