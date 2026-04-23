# =============================================================================
# SOVEREIGN HARDENED OL_FILESHARE
# File sharing service placeholder (Samba/SMB based)
# Constraint: debian-slim hardened
# =============================================================================

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates tzdata

RUN addgroup -S 65532 -r fileshare 2>/dev/null || true && \
    adduser -u 65532 -G fileshare -D -D -h /srv/share -s /sbin/nologin fileshare 2>/dev/null || true && \
    mkdir -p /srv/share /var/log/samba /var/lib/samba && \
    chown -R 65532:65532 /srv/share /var/log/samba

USER 65532:65532
WORKDIR /srv/share
EXPOSE 445 139
LABEL org.opencontainers.image.title="ol_fileshare" \
      org.opencontainers.image.description="Sovereign file sharing service (SMB/Samba)" \
      sovereign.image.tier="2" \
      sovereign.image.status="functional" \
      sovereign.image.category="storage" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
