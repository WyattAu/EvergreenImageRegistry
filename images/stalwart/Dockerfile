# =============================================================================
# SOVEREIGN HARDENED STALWART
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=0.9.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/ArcticLampyrid/stalwart/releases/download/v0.9.0/stalwart-x86_64-unknown-linux-musl" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/stalwart
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65534:65534
WORKDIR /app
EXPOSE 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/usr/local/bin/stalwart", "--version"]
ENTRYPOINT ["/usr/local/bin/stalwart"]
LABEL org.opencontainers.image.title="stalwart"       org.opencontainers.image.description="Stalwart Mail Server - all-in-one mail server written in Rust"       org.opencontainers.image.version="0.9.0"       org.opencontainers.image.vendor="ArcticLampyrid"       org.opencontainers.image.source="https://github.com/ArcticLampyrid/stalwart"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
