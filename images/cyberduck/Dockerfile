ARG VERSION=latest

FROM iterate-ch/cyberduck:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates
COPY --from=upstream /opt/cyberduck /opt/cyberduck
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/cyberduck 2>/dev/null || true

WORKDIR /app

EXPOSE 9101

LABEL org.opencontainers.image.title="cyberduck" org.opencontainers.image.version="9.1.0" org.opencontainers.image.vendor="iterate-ch" org.opencontainers.image.source="https://github.com/iterate-ch/cyberduck" evergreen.image.tier="2" evergreen.image.category="storage" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.base="wolfi" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="5s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="15000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/opt/cyberduck/Cyberduck"]
