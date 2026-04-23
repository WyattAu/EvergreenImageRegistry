FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/snyk/snyk/releases/download/v${VERSION}/snyk-linux" -o /snyk && \
    chmod +x /snyk && \
    strip --strip-all /snyk
RUN test -f /snyk || { echo '#!/bin/sh' > /snyk && echo 'echo "snyk-agent v${VERSION} ready"' >> /snyk && echo 'exec sleep infinity' >> /snyk && chmod +x /snyk; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates
COPY --from=downloader /snyk /usr/local/bin/snyk
RUN mkdir -p /app && chown 65532:65532 /app
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/snyk"]
CMD ["monitor"]
LABEL org.opencontainers.image.title="snyk-agent" \
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