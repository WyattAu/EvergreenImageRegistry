ARG VERSION=latest

FROM hlebalbau/kafka-manager:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION
RUN apk add --no-cache ca-certificates curl && \
    adduser -u 65532 -s /bin/false cmak 2>/dev/null || true && \
    mkdir -p /opt/cmak/logs /var/log/cmak /var/cache/cmak 2>/dev/null || true
COPY --from=upstream /opt/cmak /opt/cmak

WORKDIR /opt/cmak

EXPOSE 9000
EXPOSE 9101

LABEL org.opencontainers.image.title="kafka-manager" org.opencontainers.image.description="Evergreen hardened CMAK (Kafka Manager) - Apache Kafka management tool" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.vendor="Yahoo" evergreen.image.tier="1" evergreen.image.status="functional" evergreen.image.category="messaging" evergreen.constraint.nonroot="true" evergreen.constraint.base="wolfi" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="15s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="30000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9000/ || exit 1
ENTRYPOINT ["/opt/cmak/bin/cmak"]
