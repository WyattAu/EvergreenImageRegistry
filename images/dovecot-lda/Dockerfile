# =============================================================================
# SOVEREIGN HARDENED DOVECOT-LDA
# Constraint: debian-slim - Dovecot LDA mode for local delivery
# =============================================================================

ARG VERSION=2.3.21
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN groupadd -r -g 65534 dovecot && useradd -r -u 65534 -g dovecot -d /var/lib/dovecot -s /usr/sbin/nologin dovecot

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        dovecot-core="2.3.*" \
        dovecot-imapd="2.3.*" \
        dovecot-lmtpd="2.3.*" \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /var/lib/dovecot /var/log/dovecot /var/mail && \
    chown -R 65534:65534 /var/lib/dovecot /var/log/dovecot /var/mail
USER 65534:65534
WORKDIR /var/lib/dovecot
EXPOSE 143 993
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["dovecot", "--version"]
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
