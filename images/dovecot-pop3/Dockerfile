# =============================================================================
# EVERGREEN HARDENED DOVECOT-POP3
# Constraint: debian-slim - Dovecot POP3 mode
# =============================================================================

ARG VERSION=2.3.21
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN groupadd -r -g 65532 dovecot && useradd -r -u 65532 -g dovecot -d /var/lib/dovecot -s /usr/bin/false dovecot


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /var/lib/dovecot /var/log/dovecot /var/mail ; \
    chown -R 65532:65532 /var/lib/dovecot /var/log/dovecot /var/mail
USER 65532:65532
WORKDIR /var/lib/dovecot
EXPOSE 110 995

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:110"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="dovecot-pop3" \
      org.opencontainers.image.description="Dovecot POP3 - Dovecot in POP3 mode" \
      org.opencontainers.image.version="2.3.21" \
      org.opencontainers.image.vendor="Dovecot" \
      org.opencontainers.image.source="https://www.dovecot.org" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian-slim="true" \
      evergreen.image.variant="pop3"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
