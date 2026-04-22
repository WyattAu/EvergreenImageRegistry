# =============================================================================
# SOVEREIGN HARDENED MAILHOG
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=1.0.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/mailhog/MailHog/releases/download/v1.0.1/MailHog_linux_amd64" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/MailHog
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65534:65534
WORKDIR /app
EXPOSE 8025 1025
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/usr/local/bin/MailHog", "--version"]
ENTRYPOINT ["/usr/local/bin/MailHog"]
LABEL org.opencontainers.image.title="mailhog"       org.opencontainers.image.description="MailHog - email testing tool"       org.opencontainers.image.version="1.0.1"       org.opencontainers.image.vendor="MailHog"       org.opencontainers.image.source="https://github.com/mailhog/MailHog"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
