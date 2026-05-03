ARG VERSION=latest

FROM ghcr.io/chart-db/chartdb:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION
ARG TARGETARCH
RUN apk add --no-cache ca-certificates
RUN adduser -D -u 65532 -s /bin/false chartdb 2>/dev/null || true
RUN mkdir -p /var/lib/chartdb /var/log/chartdb /var/cache/chartdb /opt 2>/dev/null || true
COPY --from=upstream /app /opt/chartdb
RUN chown -R 65532:65532 /opt/chartdb /var/lib/chartdb /var/log/chartdb /var/cache/chartdb 2>/dev/null || true

WORKDIR /opt/chartdb

EXPOSE 8080
EXPOSE 9101

LABEL org.opencontainers.image.title="chartdb" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Evergreen hardened ChartDB - database schema visualization tool" org.opencontainers.image.vendor="ChartDB" evergreen.image.tier="1" evergreen.image.category="database" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["java", "-jar", "/opt/chartdb/chartdb.jar"]
