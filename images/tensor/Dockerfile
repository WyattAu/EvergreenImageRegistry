# =============================================================================
# SOVEREIGN HARDENED TENSOR
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=0.2.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/mautrix/tensor/releases/download/v0.2.0/tensor-linux-amd64" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/tensor
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65534:65534
WORKDIR /app
EXPOSE 8008
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/usr/local/bin/tensor", "--version"]
ENTRYPOINT ["/usr/local/bin/tensor"]
LABEL org.opencontainers.image.title="tensor"       org.opencontainers.image.description="Tensor - Matrix federation gateway"       org.opencontainers.image.version="0.2.0"       org.opencontainers.image.vendor="mautrix"       org.opencontainers.image.source="https://github.com/mautrix/tensor"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
