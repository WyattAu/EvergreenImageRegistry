ARG VERSION=latest

FROM apache/druid:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION
RUN apk add --no-cache ca-certificates python3 && \
    adduser -D -u 65532 -s /bin/false druid 2>/dev/null || true && \
    mkdir -p /var/lib/druid /var/log/druid /var/cache/druid /opt 2>/dev/null || true
COPY --from=upstream /opt/druid /opt/druid
RUN chown -R druid:druid /opt/druid /var/lib/druid /var/log/druid /var/cache/druid 2>/dev/null || true

WORKDIR /opt/druid

EXPOSE 8088 8888 8280
EXPOSE 9101

LABEL org.opencontainers.image.title="druid" org.opencontainers.image.version="29.0.1" org.opencontainers.image.vendor="Apache" org.opencontainers.image.description="Evergreen hardened Apache Druid - real-time analytics database" evergreen.image.tier="1" evergreen.image.category="database" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8088/ || exit 1
ENTRYPOINT ["/opt/druid/bin/start-druid"]
