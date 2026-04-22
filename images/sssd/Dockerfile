# =============================================================================
# SOVEREIGN HARDENED SSSD
# System Security Services Daemon (LDAP/Kerberos authentication)
# Constraint: debian-slim hardened
# =============================================================================

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apt-get update && apt-get install -y --no-install-recommends \
        sssd sssd-ldap sssd-krb5 sssd-common \
        ca-certificates tzdata krb5-user libnss-sss libpam-sss && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN mkdir -p /var/lib/sss /var/log/sssd /etc/sssd && \
    chown -R root:root /var/lib/sss /var/log/sssd /etc/sssd && \
    chmod 700 /var/lib/sss /var/log/sssd /etc/sssd

EXPOSE 0
LABEL org.opencontainers.image.title="sssd" \
      org.opencontainers.image.description="Sovereign SSSD - System Security Services Daemon for LDAP/Kerberos auth" \
      sovereign.image.tier="2" \
      sovereign.image.status="functional" \
      sovereign.image.category="auth" \
      sovereign.image.note="SSSD requires privileged mode for PAM/NSS integration. Runs as root for PAM module access."

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM
