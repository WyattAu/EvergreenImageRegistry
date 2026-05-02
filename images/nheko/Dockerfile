ARG VERSION=latest

FROM ghcr.io/nheko-reborn/nheko:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates glib
RUN mkdir -p /app 2>/dev/null || true
RUN addgroup -S -g 10000 nheko 2>/dev/null || true ; adduser -u 65532 -G nheko -D -h /app -s /bin/false nheko
RUN mkdir -p /usr/local/bin 2>/dev/null || true
COPY --from=upstream /usr/local/bin/nheko /usr/local/bin/nheko
RUN mkdir -p /app /home/nheko/.config/nheko && chown -R 65532:65532 /app /home/nheko 2>/dev/null || true

WORKDIR /app

EXPOSE 8080
EXPOSE 9101

LABEL org.opencontainers.image.title="nheko" org.opencontainers.image.description="Nheko - desktop Matrix client (Qt/C++)" org.opencontainers.image.version="2.4.0" org.opencontainers.image.vendor="Nheko" org.opencontainers.image.source="https://github.com/Nheko-Reborn/nheko" sovereign.image.tier="2" sovereign.constraint.nonroot="true" sovereign.constraint.debian-slim="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["nheko"]
