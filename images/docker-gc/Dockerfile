ARG VERSION=0.3.0
ARG BUILD_DATE

FROM docker.io/spotify/docker-gc:latest AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates docker-cli bash || true
RUN mkdir -p /app /tmp/gc /var/lib/docker-gc 2>/dev/null || true
COPY --from=upstream /docker-gc /usr/local/bin/docker-gc
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false dockergc 2>/dev/null || true && \
    chown -R 65532:65532 /app /tmp/gc /var/lib/docker-gc 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["docker-gc"]
LABEL org.opencontainers.image.title="docker-gc" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Docker garbage collection - automatic cleanup of unused containers and images" \
      org.opencontainers.image.source="https://github.com/spotify/docker-gc" \
      sovereign.image.tier="3" \
      sovereign.image.category="devops" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
