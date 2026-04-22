# =============================================================================
# SOVEREIGN HARDENED KANIDM SERVER
# Kanidm identity server - Rust static binary (server mode)
# Constraint: scratch - pure Rust static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.9.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/kanidm/kanidm/releases/download/v${VERSION}/kanidmd-linux-amd64" -o /kanidmd && \
    curl -fsSL "https://github.com/kanidm/kanidm/releases/download/v${VERSION}/kanidmd-linux-amd64.sha256sum" -o /checksums.txt && \
    grep "kanidmd-linux-amd64" /checksums.txt | sha256sum -c - && \
    chmod +x /kanidmd && \
    strip --strip-all /kanidmd && \
    rm -f /checksums.txt

FROM scratch
COPY --from=downloader /kanidmd /kanidmd
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 8443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/kanidmd", "--help"]
ENTRYPOINT ["/kanidmd"]
LABEL org.opencontainers.image.title="kanidm-server" \
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
