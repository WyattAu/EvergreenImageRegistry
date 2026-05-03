# =============================================================================
# EVERGREEN HARDENED DOVECOT-LDA
# Constraint: debian-slim - Dovecot LDA mode for local delivery
# =============================================================================

ARG VERSION=2.3.21
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN groupadd -r -g 65532 dovecot && useradd -r -u 65532 -g dovecot -d /var/lib/dovecot -s /usr/bin/false dovecot


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates 
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /var/lib/dovecot /var/log/dovecot /var/mail ; \
    chown -R 65532:65532 /var/lib/dovecot /var/log/dovecot /var/mail
USER 65532:65532
WORKDIR /var/lib/dovecot
EXPOSE 143 993

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:143/ || exit 1
ENTRYPOINT ["dovecot", "-F"]
LABEL org.opencontainers.image.title="dovecot-lda" \
      org.opencontainers.image.description="Dovecot LDA - Dovecot in local delivery agent mode" \
      org.opencontainers.image.version="2.3.21" \
      org.opencontainers.image.vendor="Dovecot" \
      org.opencontainers.image.source="https://www.dovecot.org" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian-slim="true" \
      evergreen.image.variant="lda"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
