# =============================================================================
# SOVEREIGN HARDENED POSTFIX-RELAY
# Constraint: debian-slim - Postfix MTA for relay-only operation
# =============================================================================

ARG VERSION=3.7.6
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN groupadd -r -g 65534 postfix && useradd -r -u 65534 -g postfix -d /var/spool/postfix -s /usr/sbin/nologin postfix

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postfix="3.7.*" \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /var/spool/postfix /var/log/postfix /etc/postfix && \
    chown -R 65534:65534 /var/spool/postfix /var/log/postfix
RUN printf 'inet_interfaces = all\nrelay_domains = $mydestination\nsmtpd_relay_restrictions = permit_mynetworks, reject_unauth_destination\n' > /etc/postfix/main.cf.relay
USER 65534:65534
WORKDIR /var/spool/postfix
EXPOSE 25 587
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["postconf", "-n"]
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
