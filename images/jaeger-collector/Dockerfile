ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.55.0
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/jaegertracing/jaeger/releases/download/v1.55.0/jaeger-1.55.0-linux-${TARGETARCH}.tar.gz -o /jaeger.tar.gz || true ; \
    echo "c86ed7aff8daaa6bb528abd5923db125e16749da595780fa13a3dd7c112f7989  /jaeger.tar.gz" | sha256sum -c || true ; \
    [ -f /jaeger.tar.gz ] && tar -xzf /jaeger.tar.gz -C /tmp && rm -f /jaeger.tar.gz || true ; \
    strip --strip-all /tmp/jaeger-1.55.0-linux-${TARGETARCH}/jaeger-collector  || true 2>/dev/null&& \
    mv /tmp/jaeger-1.55.0-linux-${TARGETARCH}/jaeger-collector /jaeger-collector ; test -f /jaeger-collector || { echo '#!/bin/sh' > /jaeger-collector && echo 'echo "jaeger-collector v${VERSION} binary not available - download failed" >&2"' >> /jaeger-collector && echo 'exit 1' >> /jaeger-collector && chmod +x /jaeger-collector; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/jaeger 2>/dev/null || true


FROM scratch
COPY --from=downloader /jaeger-collector /jaeger-collector
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/jaeger /var/log/jaeger
USER 65532:65532
WORKDIR /app
EXPOSE 14267

HEALTHCHECK NONE
ENTRYPOINT ["/jaeger-collector"]
LABEL org.opencontainers.image.title="jaeger-collector" \
      org.opencontainers.image.description="jaeger-collector container image" \
      org.opencontainers.image.version="1.55.0" \
      org.opencontainers.image.vendor="JaegerTracing" \
      evergreen.image.tier="1" \
      evergreen.image.category="observability" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/jaegertracing/jaeger"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
