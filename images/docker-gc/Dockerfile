ARG VERSION=0.3.0
ARG TARGETARCH
ARG BUILD_DATE

FROM docker.io/spotify/docker-gc@sha256:0fc5d80c11902c3784efddb45573420531546c9a605c9f7245504bbf0dde3044 AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=0.3.0
RUN apk add --no-cache ca-certificates docker-cli bash || true && \
    mkdir -p /app /tmp/gc /var/lib/docker-gc 2>/dev/null || true
COPY --from=upstream /docker-gc /usr/local/bin/docker-gc
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false dockergc 2>/dev/null || true && \
    chown -R 65532:65532 /app /tmp/gc /var/lib/docker-gc 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["docker-gc"]
LABEL org.opencontainers.image.title="docker-gc" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Docker garbage collection - automatic cleanup of unused containers and images" \
      org.opencontainers.image.source="https://github.com/spotify/docker-gc" \
      evergreen.image.tier="3" \
      evergreen.image.category="devops" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
