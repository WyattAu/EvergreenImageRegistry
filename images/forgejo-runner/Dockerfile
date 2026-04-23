FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://codeberg.org/forgejo/runner/releases/download/v6.1.0/forgejo-runner-6.1.0-linux-amd64" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary




FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/forgejo-runner
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65532:65532
WORKDIR /app
EXPOSE 8080
LABEL org.opencontainers.image.title="forgejo-runner"       org.opencontainers.image.description="Forgejo Act Runner - CI/CD runner for Forgejo"       org.opencontainers.image.version="6.1.0"       org.opencontainers.image.vendor="Forgejo"       org.opencontainers.image.source="https://codeberg.org/forgejo/runner"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM