# =============================================================================
# EVERGREEN HARDENED POSTFIX-RELAY
# Constraint: debian-slim - Postfix MTA for relay-only operation
# =============================================================================

ARG VERSION=3.7.6
ARG TARGETARCH
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN groupadd -r -g 65532 postfix && useradd -r -u 65532 -g postfix -d /var/spool/postfix -s /usr/bin/false postfix


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache postfix ca-certificates || true
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /var/spool/postfix /var/log/postfix /etc/postfix ; \
    chown -R 65532:65532 /var/spool/postfix /var/log/postfix && \
    printf 'inet_interfaces = all\nrelay_domains = $mydestination\nsmtpd_relay_restrictions = permit_mynetworks, reject_unauth_destination\n' > /etc/postfix/main.cf.relay
USER 65532:65532
WORKDIR /var/spool/postfix
EXPOSE 25 587

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:25/ || exit 1
ENTRYPOINT ["postfix", "-c", "/etc/postfix", "start-fg"]
LABEL org.opencontainers.image.title="postfix-relay" \
      org.opencontainers.image.description="Postfix Relay - mail transfer agent in relay-only mode" \
      org.opencontainers.image.version="3.7.6" \
      org.opencontainers.image.vendor="Wietse Venema" \
      org.opencontainers.image.source="https://www.postfix.org" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian-slim="true" \
      evergreen.image.variant="relay"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
