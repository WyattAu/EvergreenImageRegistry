# =============================================================================
# SOVEREIGN HARDENED POSTFIX
# Constraint: debian-slim - package-based runtime for system services
# =============================================================================

ARG VERSION=3.7.6
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN groupadd -r -g 65534 appuser && useradd -r -u 65534 -g appuser -d /app -s /usr/sbin/nologin appuser

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends postfix="3.7.6-*" mailutils="1:3.7-*" &&     rm -rf /var/lib/apt/lists/*
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /app /var/log/postfix /var/cache/postfix && chown -R 65534:65534 /app /var/log/postfix /var/cache/postfix
USER 65534:65534
WORKDIR /app
EXPOSE 25
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["postconf", "-n"]
LABEL org.opencontainers.image.title="postfix"       org.opencontainers.image.description="Postfix - mail transfer agent"       org.opencontainers.image.version="3.7.6"       org.opencontainers.image.vendor="Wietse Venema"       org.opencontainers.image.source="https://www.postfix.org"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian-slim="true"
