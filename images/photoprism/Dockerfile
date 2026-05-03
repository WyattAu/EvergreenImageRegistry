ARG VERSION=260305-fad9d5395

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL \
    "https://github.com/photoprism/photoprism/releases/download/${VERSION}/photoprism_${VERSION}-linux-amd64.tar.gz" \
    -o /tmp/photoprism.tar.gz && \
    tar -xzf /tmp/photoprism.tar.gz -C /opt && rm -f /tmp/photoprism.tar.gz && \
    chmod +x /opt/photoprism 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION
RUN apk add --no-cache ca-certificates
COPY --from=downloader /opt/photoprism /opt/photoprism
RUN adduser -u 65532 -D photoprism 2>/dev/null || true
RUN mkdir -p /app /var/log/photoprism /var/cache/photoprism && chown -R 65532:65532 /app /var/log/photoprism /var/cache/photoprism /opt/photoprism
USER 65532:65532
WORKDIR /app
EXPOSE 2282

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:2282/ || exit 1
ENTRYPOINT ["/opt/photoprism"]
LABEL org.opencontainers.image.title="photoprism"       org.opencontainers.image.version="260305-fad9d5395"       org.opencontainers.image.vendor="PhotoPrism"       evergreen.image.tier="2"       evergreen.constraint.nonroot="true"       evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
