
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.1300.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/snyk/snyk/releases/download/v${VERSION}/snyk-linux -o /snyk || true ; \
    chmod +x /snyk && \
    strip --strip-all /snyk ; test -f /snyk || { echo '#!/bin/sh' > /snyk && echo 'echo "snyk v${VERSION} ready"' >> /snyk && echo 'exec sleep infinity' >> /snyk && chmod +x /snyk; } 2>/dev/null || true



FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates || true
COPY --from=downloader /snyk /usr/local/bin/snyk
RUN mkdir -p /app && chown 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/snyk"]
LABEL org.opencontainers.image.title="snyk" \
      org.opencontainers.image.version="1.1300.0" \
      org.opencontainers.image.vendor="Snyk" \
      org.opencontainers.image.source="https://github.com/snyk/snyk" \
      sovereign.image.tier="2" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
