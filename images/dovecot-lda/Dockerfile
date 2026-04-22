# =============================================================================
# SOVEREIGN HARDENED DOVECOT-LDA
# Constraint: debian-slim - Dovecot LDA mode for local delivery
# =============================================================================

ARG VERSION=2.3.21
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN groupadd -r -g 65532 dovecot && useradd -r -u 65532 -g dovecot -d /var/lib/dovecot -s /usr/sbin/nologin dovecot

FROM cgr.dev/chainguard/wolfi-base:latest

SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apk add --no-cache ca-certificates
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /var/lib/dovecot /var/log/dovecot /var/mail && \
    chown -R 65532:65532 /var/lib/dovecot /var/log/dovecot /var/mail
USER 65532:65532
WORKDIR /var/lib/dovecot
EXPOSE 143 993
ENTRYPOINT ["dovecot", "-F"]
LABEL org.opencontainers.image.title="dovecot-lda" \
      org.opencontainers.image.description="Dovecot LDA - Dovecot in local delivery agent mode" \
      org.opencontainers.image.version="2.3.21" \
      org.opencontainers.image.vendor="Dovecot" \
      org.opencontainers.image.source="https://www.dovecot.org" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true" \
      sovereign.image.variant="lda"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM