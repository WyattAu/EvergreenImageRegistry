FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
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

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
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

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:80/ || exit 1
ENTRYPOINT ["busybox", "httpd", "-f", "-p", "80", "-h", "/app"]
LABEL org.opencontainers.image.title="element-web" \
      org.opencontainers.image.description="Element Web - web client for Matrix" \
      org.opencontainers.image.version="1.11.14" \
      org.opencontainers.image.vendor="Element" \
      org.opencontainers.image.source="https://github.com/element-hq/element-web" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
