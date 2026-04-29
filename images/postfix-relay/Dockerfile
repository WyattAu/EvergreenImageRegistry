# =============================================================================
# SOVEREIGN HARDENED POSTFIX-RELAY
# Constraint: debian-slim - Postfix MTA for relay-only operation
# =============================================================================

ARG VERSION=3.7.6
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN groupadd -r -g 65532 postfix && useradd -r -u 65532 -g postfix -d /var/spool/postfix -s /usr/bin/false postfix


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache postfix ca-certificates || true
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /var/spool/postfix /var/log/postfix /etc/postfix ; \
    chown -R 65532:65532 /var/spool/postfix /var/log/postfix
RUN printf 'inet_interfaces = all
nrelay_domains = $mydestination
nsmtpd_relay_restrictions = permit_mynetworks, reject_unauth_destination
n' > /etc/postfix/main.cf.relay
USER 65532:65532
WORKDIR /var/spool/postfix
EXPOSE 25 587
ENTRYPOINT ["postfix", "-c", "/etc/postfix", "start-fg"]
LABEL org.opencontainers.image.title="postfix-relay" \
      org.opencontainers.image.description="Postfix Relay - mail transfer agent in relay-only mode" \
      org.opencontainers.image.version="3.7.6" \
      org.opencontainers.image.vendor="Wietse Venema" \
      org.opencontainers.image.source="https://www.postfix.org" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true" \
      sovereign.image.variant="relay"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM