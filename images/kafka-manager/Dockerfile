ARG VERSION=latest

FROM hlebalbau/kafka-manager:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates curl
RUN adduser -u 65532 -s /bin/false cmak 2>/dev/null || true
RUN mkdir -p /opt/cmak/logs /var/log/cmak /var/cache/cmak 2>/dev/null || true
COPY --from=upstream /opt/cmak /opt/cmak

WORKDIR /opt/cmak

EXPOSE 9000
EXPOSE 9101

LABEL org.opencontainers.image.title="kafka-manager" org.opencontainers.image.description="Sovereign hardened CMAK (Kafka Manager) - Apache Kafka management tool" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.vendor="Yahoo" sovereign.image.tier="1" sovereign.image.status="functional" sovereign.image.category="messaging" sovereign.constraint.nonroot="true" sovereign.constraint.base="wolfi" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="15s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/opt/cmak/bin/cmak"]
