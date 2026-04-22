# =============================================================================
# SOVEREIGN HARDENED OL_FILESHARE
# File sharing service placeholder (Samba/SMB based)
# Constraint: debian-slim hardened
# =============================================================================

FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates tzdata samba-common-bin samba-daemon && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN groupadd -g 65534 -r fileshare 2>/dev/null || true && \
    useradd -r -u 65534 -g fileshare -d /srv/share -s /sbin/nologin fileshare 2>/dev/null || true && \
    mkdir -p /srv/share /var/log/samba /var/lib/samba && \
    chown -R 65534:65534 /srv/share /var/log/samba

USER 65534:65534
WORKDIR /srv/share
EXPOSE 445 139
LABEL org.opencontainers.image.title="ol_fileshare" \
      org.opencontainers.image.description="Sovereign file sharing service (SMB/Samba)" \
      sovereign.image.tier="2" \
      sovereign.image.status="functional" \
      sovereign.image.category="storage" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
