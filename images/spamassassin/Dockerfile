# =============================================================================
# SOVEREIGN HARDENED SPAMASSASSIN
# Constraint: debian-slim - package-based runtime for system services
# =============================================================================

ARG VERSION=4.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN groupadd -r -g 65534 appuser && useradd -r -u 65534 -g appuser -d /app -s /usr/sbin/nologin appuser

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends spamassassin="4.0.*" spamc="4.0.*" &&     rm -rf /var/lib/apt/lists/*
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
RUN mkdir -p /app /var/log/spamassassin /var/cache/spamassassin && chown -R 65534:65534 /app /var/log/spamassassin /var/cache/spamassassin
USER 65534:65534
WORKDIR /app
EXPOSE 783
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["spamassassin", "--version"]
LABEL org.opencontainers.image.title="spamassassin"       org.opencontainers.image.description="SpamAssassin - email spam filter"       org.opencontainers.image.version="4.0.0"       org.opencontainers.image.vendor="Apache"       org.opencontainers.image.source="https://spamassassin.apache.org"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian-slim="true"
