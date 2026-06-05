ARG VERSION=10.8.14
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM ontotext/graphdb:${VERSION} AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=v8.5.6
RUN apk add --no-cache ca-certificates && \
    adduser -D -u 65532 -s /bin/false graphdb 2>/dev/null || true && \
    mkdir -p /var/lib/graphdb /var/log/graphdb /var/cache/graphdb /opt/graphdb/home /opt 2>/dev/null || true
COPY --from=upstream /opt/graphdb /opt/graphdb
RUN chown -R 65532:65532 /opt/graphdb /var/lib/graphdb /var/log/graphdb /var/cache/graphdb 2>/dev/null || true

WORKDIR /opt/graphdb

EXPOSE 7200
EXPOSE 9101

LABEL org.opencontainers.image.title="graphdb-enterpriser" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Evergreen hardened GraphDB Enterprise - semantic graph database" org.opencontainers.image.vendor="Ontotext" evergreen.image.tier="1" evergreen.image.category="database" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.base.image="wolfi" \
      org.opencontainers.image.source="https://github.com/ontotext/graphdb"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:7200"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
