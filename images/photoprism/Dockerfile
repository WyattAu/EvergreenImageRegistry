ARG VERSION=260305-fad9d5395
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=260305-fad9d5395
RUN mkdir -p /opt/photoprism || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL \
    "https://github.com/photoprism/photoprism/releases/download/${VERSION}/photoprism_${VERSION}-linux-${TARGETARCH}.tar.gz" \
    -o /tmp/photoprism.tar.gz && \
    tar -xzf /tmp/photoprism.tar.gz -C /opt && rm -f /tmp/photoprism.tar.gz && \
    chmod +x /opt/photoprism 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=260305-fad9d5395
RUN apk add --no-cache ca-certificates
COPY --from=downloader /opt/photoprism /opt/photoprism
RUN adduser -u 65532 -D photoprism 2>/dev/null || true && \
    mkdir -p /app /var/log/photoprism /var/cache/photoprism && chown -R 65532:65532 /app /var/log/photoprism /var/cache/photoprism /opt/photoprism
USER 65532:65532
WORKDIR /app
EXPOSE 2282

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:2282/ || exit 1
ENTRYPOINT ["/opt/photoprism"]
LABEL org.opencontainers.image.title="photoprism"       org.opencontainers.image.version="260305-fad9d5395"       org.opencontainers.image.vendor="PhotoPrism"       evergreen.image.tier="2"       evergreen.constraint.nonroot="true"       evergreen.base.image="wolfi" \
      org.opencontainers.image.source="https://github.com/photoprism/photoprism" \
      org.opencontainers.image.description="photoprism container image" \
evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
