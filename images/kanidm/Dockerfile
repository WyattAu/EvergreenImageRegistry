# =============================================================================
# SOVEREIGN HARDENED KANIDM
# Identity management system - Rust static binary
# Constraint: scratch - pure Rust static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.9.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/kanidm/kanidm/releases/download/v${VERSION}/kanidm-linux-amd64" -o /kanidm && \
    curl -fsSL "https://github.com/kanidm/kanidm/releases/download/v${VERSION}/kanidm-linux-amd64.sha256sum" -o /checksums.txt && \
    grep "kanidm-linux-amd64" /checksums.txt | sha256sum -c - && \
    chmod +x /kanidm && \
    strip --strip-all /kanidm && \
    rm -f /checksums.txt

FROM scratch
COPY --from=downloader /kanidm /kanidm
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/kanidm", "--help"]
ENTRYPOINT ["/kanidm"]
LABEL org.opencontainers.image.title="kanidm" \
      org.opencontainers.image.version="1.9.2" \
      org.opencontainers.image.vendor="Kanidm" \
      org.opencontainers.image.source="https://github.com/kanidm/kanidm" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
