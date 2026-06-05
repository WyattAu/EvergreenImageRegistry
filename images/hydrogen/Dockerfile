ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=0.5.1
ARG TARGETARCH
RUN mkdir -p /www-src || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 --connect-timeout 30 --max-time 300 -fsSL "https://github.com/element-hq/hydrogen-web/releases/download/v${VERSION}/hydrogen-web-${VERSION}.tar.gz" -o /hydrogen.tar.gz 2>/dev/null ; \
    echo "ee9bd7cf330a8d6cc95e00ce37b89f5437656ee1aff92821ded2c4d6611306a0  /hydrogen.tar.gz" | sha256sum -c ; \
    mkdir -p /www-src && if [ -f /hydrogen.tar.gz ]; then tar -xzf /hydrogen.tar.gz -C /www-src --strip-components=1 2>/dev/null ; rm -f /hydrogen.tar.gz 2>/dev/null ; fi
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=0.5.1
RUN apk add --no-cache ca-certificates busybox && \
    addgroup -S -g 10000 hydrogen 2>/dev/null || true && adduser -u 65532 -G hydrogen -D -h /app -s /bin/false hydrogen 2>/dev/null || true && \
    mkdir -p /app 2>/dev/null || true
COPY --from=builder /www-src /app
RUN chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="hydrogen" \
      org.opencontainers.image.version="0.5.1" \
      org.opencontainers.image.vendor="Element" \
      org.opencontainers.image.source="https://github.com/element-hq/hydrogen-web" \
      org.opencontainers.image.description="Hydrogen - lightweight Matrix web client" \
      evergreen.image.tier="2" \
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
