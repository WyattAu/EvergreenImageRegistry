ARG VERSION=1.35.8

FROM vaultwarden/server:1.35.8 AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates 
COPY --from=upstream /vaultwarden /usr/local/bin/vaultwarden
RUN mkdir -p /app && chown 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/vaultwarden"]
CMD ["--database-url", "mysql://user:pass@host/db"]
LABEL org.opencontainers.image.title="vaultwarden-mysql"       org.opencontainers.image.version="1.35.8"       org.opencontainers.image.vendor="dani-garcia"       org.opencontainers.image.source="https://github.com/dani-garcia/vaultwarden"       sovereign.image.tier="2"       sovereign.image.category="secrets"       sovereign.image.status="functional"       sovereign.constraint.nonroot="true"       sovereign.constraint.base="wolfi"       sovereign.hft.signal-handling="native"       sovereign.hft.shutdown-timeout="3s"       sovereign.hft.init-system="none"       sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
