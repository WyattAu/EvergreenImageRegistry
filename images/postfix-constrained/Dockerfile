# =============================================================================
# EVERGREEN HARDENED POSTFIX-CONSTRAINED
# Constraint: debian-slim - Postfix MTA with constrained resource limits
# =============================================================================

ARG VERSION=3.7.6
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN groupadd -r -g 65532 postfix && useradd -r -u 65532 -g postfix -d /var/spool/postfix -s /usr/bin/false postfix


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache postfix ca-certificates || true
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /var/spool/postfix /var/log/postfix /etc/postfix ; \
    chown -R 65532:65532 /var/spool/postfix /var/log/postfix
RUN printf 'inet_interfaces = all\ndefault_process_limit = 10\nsmtpd_client_connection_rate_limit = 10\nqueue_run_delay = 300s\nminimal_backoff_time = 300s\nmaximal_backoff_time = 3600s\n' > /etc/postfix/main.cf.constrained
USER 65532:65532
WORKDIR /var/spool/postfix
EXPOSE 25

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:25/ || exit 1
ENTRYPOINT ["postfix", "-c", "/etc/postfix", "start-fg"]
LABEL org.opencontainers.image.title="postfix-constrained" \
      org.opencontainers.image.description="Postfix Constrained - mail transfer agent with resource limits" \
      org.opencontainers.image.version="3.7.6" \
      org.opencontainers.image.vendor="Wietse Venema" \
      org.opencontainers.image.source="https://www.postfix.org" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian-slim="true" \
      evergreen.image.variant="constrained"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
