ARG VERSION=2.31.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        skrooge \
        ca-certificates curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/app /var/cache/app \
    && chown -R 65532:65532 /app /var/log/app /var/cache/app
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["skrooge"]
LABEL org.opencontainers.image.title="skrooge" \
      org.opencontainers.image.version="2.31.0" \
      org.opencontainers.image.vendor="Skrooge" \
      org.opencontainers.image.source="https://github.com/skrooge/skrooge" \
      sovereign.image.tier="2" \
      sovereign.image.category="business-finance" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM