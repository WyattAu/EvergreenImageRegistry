# =============================================================================
# SOVEREIGN HARDENED COURIER-AUTHLIB
# Constraint: debian-slim - package-based runtime for system services
# =============================================================================

ARG VERSION=0.71.4
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN groupadd -r -g 65534 appuser && useradd -r -u 65534 -g appuser -d /app -s /usr/sbin/nologin appuser

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends courier-authlib="0.71.4-*" &&     rm -rf /var/lib/apt/lists/*
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /app /var/log/courier-authlib /var/cache/courier-authlib && chown -R 65534:65534 /app /var/log/courier-authlib /var/cache/courier-authlib
USER 65534:65534
WORKDIR /app
EXPOSE 0
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["courierauthconfig", "--version"]
LABEL org.opencontainers.image.title="courier-authlib"       org.opencontainers.image.description="Courier Authlib - authentication library for Courier mail server"       org.opencontainers.image.version="0.71.4"       org.opencontainers.image.vendor="Courier Mail Server"       org.opencontainers.image.source="https://www.courier-mta.org/authlib"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian-slim="true"
