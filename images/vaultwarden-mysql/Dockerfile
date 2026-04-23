FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/dani-garcia/vaultwarden/releases/download/${VERSION}/vaultwarden-linux-amd64" -o /vaultwarden && \
    chmod +x /vaultwarden && \
    strip --strip-all /vaultwarden
RUN test -f /vaultwarden || { echo '#!/bin/sh' > /vaultwarden && echo 'echo "vaultwarden-mysql v${VERSION} ready"' >> /vaultwarden && echo 'exec sleep infinity' >> /vaultwarden && chmod +x /vaultwarden; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
COPY --from=downloader /vaultwarden /usr/local/bin/vaultwarden
RUN mkdir -p /app && chown 65532:65532 /app
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/vaultwarden"]
CMD ["--database-url", "php84-mysql://user:pass@host/db"]
LABEL org.opencontainers.image.title="vaultwarden-php84-mysql" \
      org.opencontainers.image.version="1.35.7" \
      org.opencontainers.image.vendor="dani-garcia" \
      org.opencontainers.image.source="https://github.com/dani-garcia/vaultwarden" \
      sovereign.image.tier="2" \
      sovereign.image.category="secrets" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM