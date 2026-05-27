ARG VERSION=7.5.1
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM sqlpad/sqlpad:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache wget ca-certificates bash
RUN mkdir -p /app /var/lib/sqlpad || true
COPY --from=upstream /docker-entrypoint /docker-entrypoint
COPY --from=upstream /usr/app /app
RUN adduser -u 65532 -s /bin/false sqlpad 2>/dev/null || true && \
    chown -R 65532:65532 /app


WORKDIR /app

EXPOSE 3000
EXPOSE 9101

LABEL org.opencontainers.image.title="sqlpad" org.opencontainers.image.version="7.5.1" org.opencontainers.image.description="SQLPad - Web-based SQL Editor with Query Visualization" org.opencontainers.image.vendor="SQLPad" org.opencontainers.image.source="https://github.com/sqlpad/sqlpad" evergreen.image.tier="1" evergreen.constraint.nonroot="true" evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:3000/ || exit 1
ENTRYPOINT ["/docker-entrypoint"]
