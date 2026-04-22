# =============================================================================
# SOVEREIGN HARDENED POSTGREY
# Constraint: debian-slim - package-based runtime for system services
# =============================================================================

ARG VERSION=1.37
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN groupadd -r -g 65534 appuser && useradd -r -u 65534 -g appuser -d /app -s /usr/sbin/nologin appuser

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends postgrey="1.37-*" postfix="3.7.*" &&     rm -rf /var/lib/apt/lists/*
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /app /var/log/postgrey /var/cache/postgrey && chown -R 65534:65534 /app /var/log/postgrey /var/cache/postgrey
USER 65534:65534
WORKDIR /app
EXPOSE 10023
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["postgrey", "--version"]
LABEL org.opencontainers.image.title="postgrey"       org.opencontainers.image.description="Postgrey - Postfix greylisting policy server"       org.opencontainers.image.version="1.37"       org.opencontainers.image.vendor="David Schweikert"       org.opencontainers.image.source="https://postgrey.schweikert.ch"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian-slim="true"
