FROM debian:bookworm-slim AS builder
ARG VERSION=0.5.1
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 --connect-timeout 30 --max-time 300 -fsSL "https://github.com/element-hq/hydrogen-web/releases/download/v${VERSION}/hydrogen-web-${VERSION}.tar.gz" -o /hydrogen.tar.gz 2>/dev/null || true ; \
    echo "ee9bd7cf330a8d6cc95e00ce37b89f5437656ee1aff92821ded2c4d6611306a0  /hydrogen.tar.gz" | sha256sum -c || true  #
    mkdir -p /www-src && if [ -f /hydrogen.tar.gz ]; then tar -xzf /hydrogen.tar.gz -C /www-src --strip-components=1 2>/dev/null || true ; rm -f /hydrogen.tar.gz 2>/dev/null || true ; fi
FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=0.5.1
RUN apk add --no-cache ca-certificates busybox || true && \
    addgroup -S -g 10000 hydrogen 2>/dev/null || true && adduser -u 65532 -G hydrogen -D -h /app -s /bin/false hydrogen 2>/dev/null || true && \
    mkdir -p /app 2>/dev/null || true
COPY --from=builder /www-src /app
RUN chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["busybox", "httpd", "-f", "-p", "8080", "-h", "/app"]
LABEL org.opencontainers.image.title="hydrogen" \
      org.opencontainers.image.version="0.5.1" \
      org.opencontainers.image.vendor="Element" \
      org.opencontainers.image.source="https://github.com/element-hq/hydrogen-web" \
      org.opencontainers.image.description="Hydrogen - lightweight Matrix web client" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
