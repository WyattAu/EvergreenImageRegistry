ARG VERSION=latest

FROM realm/mongodb-realm:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION
RUN apk add --no-cache ca-certificates curl || true && \
    adduser -D -u 65532 -s /bin/false realm 2>/dev/null || true && \
    mkdir -p /var/lib/realm /var/log/realm /var/cache/realm /opt 2>/dev/null || true
COPY --from=upstream /realm /opt/realm
RUN chown -R 65532:65532 /opt/realm /var/lib/realm /var/log/realm /var/cache/realm 2>/dev/null || true

WORKDIR /opt/realm

EXPOSE 9090
EXPOSE 9101

LABEL org.opencontainers.image.title="realm-server" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Evergreen hardened MongoDB Realm Server - application backend platform" org.opencontainers.image.vendor="MongoDB" evergreen.image.tier="1" evergreen.image.category="database" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.base.image="wolfi" \
      org.opencontainers.image.source="https://github.com/realm/realm-core"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9090/ || exit 1
ENTRYPOINT ["/opt/realm/bin/realm-server"]
