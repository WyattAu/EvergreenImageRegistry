ARG VERSION=1.35.8

FROM vaultwarden/server@sha256:c4f6056fe0c288a052a223cecd263a90d1dda1a0177bb5b054a363a6c7b211d9 AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION
RUN apk add --no-cache libpq ca-certificates
COPY --from=upstream /vaultwarden /usr/local/bin/vaultwarden
RUN mkdir -p /app && chown 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["/usr/local/bin/vaultwarden"]
CMD ["--database-url", "postgresql://user:pass@host/db"]
LABEL org.opencontainers.image.title="vaultwarden-postgres"       org.opencontainers.image.version="1.35.8"       org.opencontainers.image.vendor="dani-garcia"       org.opencontainers.image.source="https://github.com/dani-garcia/vaultwarden"       evergreen.image.tier="2"       evergreen.image.category="secrets"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.base="wolfi"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="3s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="3000ms" \
      org.opencontainers.image.description="vaultwarden-postgres container image" \
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
