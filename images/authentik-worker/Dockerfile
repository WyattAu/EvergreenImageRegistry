ARG VERSION=version/2026.2.2
ARG TARGETARCH

FROM ghcr.io/goauthentik/authentik:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates libpq libxml2-dev libxslt-dev libffi-dev openssl-dev build-base || true
COPY --from=upstream /venv /opt/authentik-worker
RUN pip install --no-cache-dir --break-system-packages /opt/authentik-worker 2>/dev/null || pip install --no-cache-dir /opt/authentik-worker || true && \
    mkdir -p /app && chown -R 65532:65532 /app /opt/authentik-worker 2>/dev/null || true

WORKDIR /app

EXPOSE 9101

LABEL org.opencontainers.image.title="authentik-worker" org.opencontainers.image.version="2026.2.2" org.opencontainers.image.vendor="goauthentik" org.opencontainers.image.source="https://github.com/goauthentik/authentik" evergreen.image.tier="2" evergreen.image.category="identity" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.base="wolfi" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="30s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="30000ms" \
      org.opencontainers.image.description="authentik-worker container image" \
evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["python3", "-m", "authentik"]

CMD ["worker"]
