ARG VERSION=latest

FROM cubrid/cubrid:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

ARG VERSION
RUN apk add --no-cache ca-certificates && \
    adduser -D -u 65532 -s /bin/false cubrid 2>/dev/null || true && \
    mkdir -p /var/lib/cubrid /var/log/cubrid /var/cache/cubrid /opt 2>/dev/null || true
COPY --from=upstream /opt/cubrid /opt/cubrid
RUN chown -R 65532:65532 /opt/cubrid /var/lib/cubrid /var/log/cubrid /var/cache/cubrid 2>/dev/null || true

WORKDIR /var/lib/cubrid

EXPOSE 30000 33000 33001
EXPOSE 9101

LABEL org.opencontainers.image.title="cubrid" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Evergreen hardened CUBRID - open source SQL database" org.opencontainers.image.vendor="CUBRID" evergreen.image.tier="1" evergreen.image.category="database" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.base.image="wolfi" \
      org.opencontainers.image.source="https://github.com/CUBRID/cubrid"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:30000/ || exit 1
ENTRYPOINT ["/opt/cubrid/bin/cubrid"]
