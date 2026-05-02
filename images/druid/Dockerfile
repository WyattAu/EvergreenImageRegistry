ARG VERSION=latest

FROM apache/druid:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates python3
RUN adduser -D -u 65532 -s /bin/false druid 2>/dev/null || true
RUN mkdir -p /var/lib/druid /var/log/druid /var/cache/druid /opt 2>/dev/null || true
COPY --from=upstream /opt/druid /opt/druid
RUN chown -R druid:druid /opt/druid /var/lib/druid /var/log/druid /var/cache/druid 2>/dev/null || true

WORKDIR /opt/druid

EXPOSE 8088 8888 8280
EXPOSE 9101

LABEL org.opencontainers.image.title="druid" org.opencontainers.image.version="29.0.1" org.opencontainers.image.vendor="Apache" org.opencontainers.image.description="Sovereign hardened Apache Druid - real-time analytics database" sovereign.image.tier="1" sovereign.image.category="database" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/opt/druid/bin/start-druid"]
