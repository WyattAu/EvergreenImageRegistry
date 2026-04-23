FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/mailhog/MailHog/releases/download/v1.0.1/MailHog_linux_amd64" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary




FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/MailHog
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65532:65532
WORKDIR /app
EXPOSE 8025 1025
LABEL org.opencontainers.image.title="mailhog"       org.opencontainers.image.description="MailHog - email testing tool"       org.opencontainers.image.version="1.0.1"       org.opencontainers.image.vendor="MailHog"       org.opencontainers.image.source="https://github.com/mailhog/MailHog"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM