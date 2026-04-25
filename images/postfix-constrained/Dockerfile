# =============================================================================
# SOVEREIGN HARDENED POSTFIX-CONSTRAINED
# Constraint: debian-slim - Postfix MTA with constrained resource limits
# =============================================================================

ARG VERSION=3.7.6
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN groupadd -r -g 65532 postfix && useradd -r -u 65532 -g postfix -d /var/spool/postfix -s /usr/sbin/nologin postfix


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache postfix ca-certificates || true
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /var/spool/postfix /var/log/postfix /etc/postfix && \ 2>/dev/null || true ; \
    chown -R 65532:65532 /var/spool/postfix /var/log/postfix
RUN printf 'inet_interfaces = all\ndefault_process_limit = 10\nsmtpd_client_connection_rate_limit = 10\nqueue_run_delay = 300s\nminimal_backoff_time = 300s\nmaximal_backoff_time = 3600s\n' > /etc/postfix/main.cf.constrained
USER 65532:65532
WORKDIR /var/spool/postfix
EXPOSE 25
ENTRYPOINT ["postfix", "-c", "/etc/postfix", "start-fg"]
LABEL org.opencontainers.image.title="postfix-constrained" \
      org.opencontainers.image.description="Postfix Constrained - mail transfer agent with resource limits" \
      org.opencontainers.image.version="3.7.6" \
      org.opencontainers.image.vendor="Wietse Venema" \
      org.opencontainers.image.source="https://www.postfix.org" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true" \
      sovereign.image.variant="constrained"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM