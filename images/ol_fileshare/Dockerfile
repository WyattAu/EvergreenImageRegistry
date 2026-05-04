# =============================================================================
# EVERGREEN HARDENED OL_FILESHARE
# Constraint: debian-slim hardened
# =============================================================================


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates tzdata && \
    addgroup -S -g 65532 fileshare 2>/dev/null || true && \
    adduser -u 65532 -G fileshare -D -D -h /srv/share -s /bin/false fileshare 2>/dev/null || true && \
    mkdir -p /srv/share /var/log/samba /var/lib/samba ; \
    chown -R 65532:65532 /srv/share /var/log/samba
USER 65532:65532
WORKDIR /srv/share
EXPOSE 445 139
LABEL org.opencontainers.image.title="ol_fileshare" \
      org.opencontainers.image.description="Evergreen file sharing service (SMB/Samba)" \
      evergreen.image.tier="2" \
      evergreen.image.status="functional" \
      evergreen.image.category="storage" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:139/ || exit 1
CMD ["/bin/sh"]
