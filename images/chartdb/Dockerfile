ARG VERSION=latest

FROM ghcr.io/chart-db/chartdb:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates
RUN adduser -D -u 65532 -s /bin/false chartdb 2>/dev/null || true
RUN mkdir -p /var/lib/chartdb /var/log/chartdb /var/cache/chartdb /opt 2>/dev/null || true
COPY --from=upstream /app /opt/chartdb
RUN chown -R 65532:65532 /opt/chartdb /var/lib/chartdb /var/log/chartdb /var/cache/chartdb 2>/dev/null || true

WORKDIR /opt/chartdb

EXPOSE 8080
EXPOSE 9101

LABEL org.opencontainers.image.title="chartdb" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Sovereign hardened ChartDB - database schema visualization tool" org.opencontainers.image.vendor="ChartDB" sovereign.image.tier="1" sovereign.image.category="database" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["java", "-jar", "/opt/chartdb/chartdb.jar"]
