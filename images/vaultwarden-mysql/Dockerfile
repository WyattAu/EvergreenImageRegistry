# =============================================================================
# SOVEREIGN HARDENED VAULTWARDEN MYSQL
# Vaultwarden with MySQL backend - Rust static binary
# Constraint: debian-slim - MySQL client libs needed for runtime
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.35.7
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/dani-garcia/vaultwarden/releases/download/${VERSION}/vaultwarden-linux-amd64" -o /vaultwarden && \
    chmod +x /vaultwarden && \
    strip --strip-all /vaultwarden

FROM debian:bookworm-slim AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends libmariadb3 ca-certificates && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /vaultwarden /usr/local/bin/vaultwarden
RUN mkdir -p /app && chown 65534:65534 /app
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/vaultwarden", "--help"]
ENTRYPOINT ["/usr/local/bin/vaultwarden"]
CMD ["--database-url", "mysql://user:pass@host/db"]
LABEL org.opencontainers.image.title="vaultwarden-mysql" \
      org.opencontainers.image.version="1.35.7" \
      org.opencontainers.image.vendor="dani-garcia" \
      org.opencontainers.image.source="https://github.com/dani-garcia/vaultwarden" \
      sovereign.image.tier="2" \
      sovereign.image.category="secrets" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
