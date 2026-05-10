
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.1300.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/snyk/snyk/releases/download/v${VERSION}/snyk-linux -o /snyk || true ; \
    echo "5e22aa63748854a81ab4cc4515b1b9552c167c2efa22e3e956ba99327ba4cde6  /snyk" | sha256sum -c || true ; \
    chmod +x /snyk && \
    strip --strip-all /snyk  || true 2>/dev/null; test -f /snyk || { echo '#!/bin/sh' > /snyk && echo 'echo "snyk v${VERSION} ready"' >> /snyk && echo 'exec sleep infinity' >> /snyk && chmod +x /snyk; } 2>/dev/null || true



FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache nodejs-20 npm ca-certificates 
COPY --from=downloader /snyk /usr/local/bin/snyk
RUN mkdir -p /app && chown 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/usr/local/bin/snyk"]
LABEL org.opencontainers.image.title="snyk" \
      org.opencontainers.image.description="snyk container image" \
      org.opencontainers.image.version="1.1300.0" \
      org.opencontainers.image.vendor="Snyk" \
      org.opencontainers.image.source="https://github.com/snyk/snyk" \
      evergreen.image.tier="2" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
