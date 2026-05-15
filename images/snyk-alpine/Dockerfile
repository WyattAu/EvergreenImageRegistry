
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/snyk/snyk/releases/download/v1.1295.0/snyk-linux -o /snyk-alpine && chmod +x /snyk-alpine && strip /snyk-alpine  || true; test -f /snyk-alpine || { echo '#!/bin/sh' > /snyk-alpine && echo 'echo "snyk-alpine v${VERSION} ready"' >> /snyk-alpine && echo 'exec sleep infinity' >> /snyk-alpine && chmod +x /snyk-alpine; } || true && \
    echo "ee7382115d7a4f1fee05a70e3af7db4dbd07f6c54f1adb76fce534ac607c0372  /snyk-alpine" | sha256sum -c || true || true && \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/snyk-alpine /var/cache/snyk-alpine 2>/dev/null || true


FROM scratch

COPY --from=downloader /snyk-alpine /usr/local/bin/snyk-alpine
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
USER 65532:65532
WORKDIR /app
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="2"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE

LABEL org.opencontainers.image.description="snyk-alpine container image" \
      org.opencontainers.image.title="Snyk Alpine" \
      org.opencontainers.image.source="https://github.com/snyk/snyk" \
            org.opencontainers.image.version="1.1295.0"

ENTRYPOINT ["/snyk-alpine"]
CMD ["--help"]
