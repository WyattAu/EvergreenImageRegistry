# =============================================================================
# SOVEREIGN HARDENED VAULTWARDEN SQLITE
# Vaultwarden with SQLite backend - Rust static binary
# Constraint: scratch - pure Rust static binary, smallest attack surface
# =============================================================================

ARG VERSION=1.35.7
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/dani-garcia/vaultwarden/releases/download/${VERSION}/vaultwarden-linux-amd64" -o /vaultwarden && \
    chmod +x /vaultwarden && \
    strip --strip-all /vaultwarden

FROM scratch
COPY --from=downloader /vaultwarden /vaultwarden
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/vaultwarden"]
CMD ["--database-url", "sqlite:///data/db.sqlite3"]
LABEL org.opencontainers.image.title="vaultwarden-sqlite" \
      org.opencontainers.image.version="1.35.7" \
      org.opencontainers.image.vendor="dani-garcia" \
      org.opencontainers.image.source="https://github.com/dani-garcia/vaultwarden" \
      sovereign.image.tier="2" \
      sovereign.image.category="secrets" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM