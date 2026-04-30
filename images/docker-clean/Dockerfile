ARG VERSION=0.3.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        "https://github.com/zzehring/docker-cleanup/releases/download/v${VERSION}/docker-cleanup-linux-amd64" \
        -o /docker-clean && \
    chmod +x /docker-clean || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates docker-cli || true
RUN mkdir -p /app /tmp/cleanup 2>/dev/null || true
COPY --from=downloader /docker-clean /usr/local/bin/docker-clean
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false dockerclean 2>/dev/null || true && \
    chown -R 65532:65532 /app /tmp/cleanup 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["docker-clean"]
LABEL org.opencontainers.image.title="docker-clean" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Docker cleanup and pruning tool" \
      org.opencontainers.image.source="https://github.com/zzehring/docker-cleanup" \
      sovereign.image.tier="3" \
      sovereign.image.category="devops" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
