FROM debian:bookworm-slim AS builder
ARG VERSION=1.11.14
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 -fsSL \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/element-hq/element-web/releases/download/v${VERSION}/element-v${VERSION}.tar.gz" \
    -o /download.tar.gz && \
    mkdir -p /www-src && \
    tar -xzf /download.tar.gz -C /www-src --strip-components=1 && \
    rm -f /download.tar.gz && \
    test -f /www-src/index.html

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=1.11.14
RUN apk add --no-cache ca-certificates busybox || true && \
    addgroup -S -g 10000 appuser 2>/dev/null || true && \
    adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser 2>/dev/null || true && \
    mkdir -p /app 2>/dev/null || true
COPY --from=builder /www-src /app
RUN chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["busybox", "httpd", "-f", "-p", "80", "-h", "/app"]
LABEL org.opencontainers.image.title="element-web" \
      org.opencontainers.image.description="Element Web - web client for Matrix" \
      org.opencontainers.image.version="1.11.14" \
      org.opencontainers.image.vendor="Element" \
      org.opencontainers.image.source="https://github.com/element-hq/element-web" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
