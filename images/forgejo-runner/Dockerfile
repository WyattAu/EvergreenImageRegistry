# =============================================================================
# SOVEREIGN HARDENED FORGEJO-RUNNER
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=6.1.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://codeberg.org/forgejo/runner/releases/download/v6.1.0/forgejo-runner-6.1.0-linux-amd64" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/forgejo-runner
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/usr/local/bin/forgejo-runner", "--version"]
ENTRYPOINT ["/usr/local/bin/forgejo-runner"]
LABEL org.opencontainers.image.title="forgejo-runner"       org.opencontainers.image.description="Forgejo Act Runner - CI/CD runner for Forgejo"       org.opencontainers.image.version="6.1.0"       org.opencontainers.image.vendor="Forgejo"       org.opencontainers.image.source="https://codeberg.org/forgejo/runner"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
