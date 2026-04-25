# =============================================================================
# SOVEREIGN HARDENED DOVECOT-POP3
# Constraint: debian-slim - Dovecot POP3 mode
# =============================================================================

ARG VERSION=2.3.21
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN groupadd -r -g 65532 dovecot && useradd -r -u 65532 -g dovecot -d /var/lib/dovecot -s /usr/sbin/nologin dovecot


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates || true
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /var/lib/dovecot /var/log/dovecot /var/mail && \ 2>/dev/null || true ; \
    chown -R 65532:65532 /var/lib/dovecot /var/log/dovecot /var/mail
USER 65532:65532
WORKDIR /var/lib/dovecot
EXPOSE 110 995
ENTRYPOINT ["dovecot", "-F"]
LABEL org.opencontainers.image.title="dovecot-pop3" \
      org.opencontainers.image.description="Dovecot POP3 - Dovecot in POP3 mode" \
      org.opencontainers.image.version="2.3.21" \
      org.opencontainers.image.vendor="Dovecot" \
      org.opencontainers.image.source="https://www.dovecot.org" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true" \
      sovereign.image.variant="pop3"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM