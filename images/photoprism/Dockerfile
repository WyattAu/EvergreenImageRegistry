ARG VERSION=260305-fad9d5395

FROM debian:bookworm-slim AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL \
    "https://github.com/photoprism/photoprism/releases/download/${VERSION}/photoprism_${VERSION}-linux-amd64.tar.gz" \
    -o /tmp/photoprism.tar.gz && \
    tar -xzf /tmp/photoprism.tar.gz -C /opt && rm -f /tmp/photoprism.tar.gz && \
    chmod +x /opt/photoprism 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates
COPY --from=downloader /opt/photoprism /opt/photoprism
RUN adduser -u 65532 -D photoprism 2>/dev/null || true
RUN mkdir -p /app /var/log/photoprism /var/cache/photoprism && chown -R 65532:65532 /app /var/log/photoprism /var/cache/photoprism /opt/photoprism
USER 65532:65532
WORKDIR /app
EXPOSE 2282
ENTRYPOINT ["/opt/photoprism"]
LABEL org.opencontainers.image.title="photoprism"       org.opencontainers.image.version="260305-fad9d5395"       org.opencontainers.image.vendor="PhotoPrism"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
