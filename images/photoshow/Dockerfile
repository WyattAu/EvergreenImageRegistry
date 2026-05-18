ARG TARGETARCH

ARG VERSION=v2

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/thibaud-rohmer/PhotoShow/archive/refs/tags/${VERSION}.tar.gz" -o /photoshow.tar.gz && \
    mkdir -p /app && tar -xzf /photoshow.tar.gz -C /app --strip-components=1 && rm -f /photoshow.tar.gz && \
    test -d /app || { echo "ERROR: failed to download photoshow" && exit 1; }

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates php php-cli php-gd php-xml php-mbstring php-json php-curl php-session && \
    addgroup -g 65532 app 2>/dev/null || true && \
    adduser -D -u 65532 -G app app 2>/dev/null || true && \
    mkdir -p /app /var/log/photoshow /var/cache/photoshow /tmp/photoshow 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/photoshow /var/cache/photoshow /tmp/photoshow 2>/dev/null || true
WORKDIR /app
COPY --from=downloader /app /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["php", "-S", "0.0.0.0:8080", "-t", "/app"]
LABEL org.opencontainers.image.title="photoshow" \
      org.opencontainers.image.description="PhotoShow - PHP gallery for browsing and sharing photos" \
      org.opencontainers.image.version="v2" \
      org.opencontainers.image.vendor="thibaud-rohmer" \
      org.opencontainers.image.source="https://github.com/thibaud-rohmer/PhotoShow" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM
