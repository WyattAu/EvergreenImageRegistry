# =============================================================================
# SOVEREIGN HARDENED FREEIPA
# Generated from template - Version: 4.12.0
# Constraint: RHEL-only - FreeIPA requires RHEL/CentOS/Fedora
# This is a stub image documenting RHEL-only availability
# =============================================================================

ARG VERSION=4.12.0
ARG BUILD_DATE

FROM scratch
LABEL org.opencontainers.image.title="freeipa" \
      org.opencontainers.image.version="4.12.0" \
      org.opencontainers.image.vendor="FreeIPA" \
      org.opencontainers.image.description="FreeIPA is RHEL/CentOS/Fedora only and cannot be built on Debian-based systems" \
      sovereign.image.tier="2" \
      sovereign.constraint.rhel_only="true" \
      sovereign.note="Install via: dnf install -y freeipa-server on RHEL/CentOS 9+"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
