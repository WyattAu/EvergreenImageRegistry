ARG VERSION=2026.2.2

FROM ghcr.io/goauthentik/authentik:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates libpq || true
COPY --from=upstream /venv /opt/authentik-geoip
RUN pip install --no-cache-dir --break-system-packages /opt/authentik-geoip 2>/dev/null || pip install --no-cache-dir /opt/authentik-geoip || true && \
    mkdir -p /app && chown -R 65532:65532 /app /opt/authentik-geoip 2>/dev/null || true

WORKDIR /app

EXPOSE 9101

LABEL org.opencontainers.image.title="authentik-geoip" org.opencontainers.image.version="2026.2.2" org.opencontainers.image.vendor="goauthentik" org.opencontainers.image.source="https://github.com/goauthentik/authentik" sovereign.image.tier="2" sovereign.image.category="identity" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.constraint.base="wolfi" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="30s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["python3", "-m", "authentik"]

CMD ["geoip"]
