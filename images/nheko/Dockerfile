ARG VERSION=0.12.1

FROM ghcr.io/nheko-reborn/nheko:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates glib && \
    mkdir -p /app 2>/dev/null || true && \
    addgroup -S -g 10000 nheko 2>/dev/null || true && adduser -u 65532 -G nheko -D -h /app -s /bin/false nheko && \
    mkdir -p /usr/local/bin 2>/dev/null || true
COPY --from=upstream /usr/local/bin/nheko /usr/local/bin/nheko
RUN mkdir -p /app /home/nheko/.config/nheko && chown -R 65532:65532 /app /home/nheko 2>/dev/null || true

WORKDIR /app

EXPOSE 8080
EXPOSE 9101

LABEL org.opencontainers.image.title="nheko" org.opencontainers.image.description="Nheko - desktop Matrix client (Qt/C++)" org.opencontainers.image.version="2.4.0" org.opencontainers.image.vendor="Nheko" org.opencontainers.image.source="https://github.com/Nheko-Reborn/nheko" evergreen.image.tier="2" evergreen.constraint.nonroot="true" evergreen.constraint.debian-slim="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["nheko"]
