ARG TARGETARCH

ARG VERSION=2025-08-05

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/RSS-Bridge/rss-bridge/archive/refs/tags/${VERSION}.tar.gz" -o /rssbridge.tar.gz && \
    mkdir -p /app && tar -xzf /rssbridge.tar.gz -C /app --strip-components=1 && rm -f /rssbridge.tar.gz && \
    test -d /app || { echo "ERROR: failed to download rss-bridge" && exit 1; }

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates php php-cli php-curl php-mbstring php-xml php-simplexml php-json php-iconv php-dom && \
    addgroup -g 65532 app 2>/dev/null || true && \
    adduser -D -u 65532 -G app app 2>/dev/null || true && \
    mkdir -p /app /var/log/rssbridge /var/cache/rssbridge 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/rssbridge /var/cache/rssbridge 2>/dev/null || true && \
    chmod -R 775 /var/cache/rssbridge 2>/dev/null || true
WORKDIR /app
COPY --from=downloader /app /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["php", "-S", "0.0.0.0:8080", "-t", "/app"]
LABEL org.opencontainers.image.title="rss2" \
      org.opencontainers.image.description="RSS-Bridge - generate RSS/Atom feeds for websites that don't have them" \
      org.opencontainers.image.version="2025-08-05" \
      org.opencontainers.image.vendor="RSS-Bridge" \
      org.opencontainers.image.source="https://github.com/RSS-Bridge/rss-bridge" \
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
