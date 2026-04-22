# =============================================================================
# SOVEREIGN HARDENED COURIER-IMAP
# Constraint: debian-slim - package-based runtime for system services
# =============================================================================

ARG VERSION=5.1.4
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN groupadd -r -g 65534 appuser && useradd -r -u 65534 -g appuser -d /app -s /usr/sbin/nologin appuser

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends courier-imap="5.1.4-*" courier-authlib="0.71.*" &&     rm -rf /var/lib/apt/lists/*
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /app /var/log/courier-imap /var/cache/courier-imap && chown -R 65534:65534 /app /var/log/courier-imap /var/cache/courier-imap
USER 65534:65534
WORKDIR /app
EXPOSE 143 993
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["courierimapd", "--version"]
LABEL org.opencontainers.image.title="courier-imap"       org.opencontainers.image.description="Courier IMAP - IMAP server"       org.opencontainers.image.version="5.1.4"       org.opencontainers.image.vendor="Courier Mail Server"       org.opencontainers.image.source="https://www.courier-mta.org/imap"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian-slim="true"
