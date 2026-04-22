# =============================================================================
# SOVEREIGN HARDENED DOVECOT
# Constraint: debian-slim - package-based runtime for system services
# =============================================================================

ARG VERSION=2.3.21
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN groupadd -r -g 65534 appuser && useradd -r -u 65534 -g appuser -d /app -s /usr/sbin/nologin appuser

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends dovecot-core="2.3.21-*" dovecot-imapd="2.3.21-*" dovecot-pop3d="2.3.21-*" dovecot-lmtpd="2.3.21-*" &&     rm -rf /var/lib/apt/lists/*
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /app /var/log/dovecot /var/cache/dovecot && chown -R 65534:65534 /app /var/log/dovecot /var/cache/dovecot
USER 65534:65534
WORKDIR /app
EXPOSE 143 993 110 995 24
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["dovecot", "--version"]
LABEL org.opencontainers.image.title="dovecot"       org.opencontainers.image.description="Dovecot - IMAP/POP3 mail server"       org.opencontainers.image.version="2.3.21"       org.opencontainers.image.vendor="Dovecot"       org.opencontainers.image.source="https://www.dovecot.org"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian-slim="true"
