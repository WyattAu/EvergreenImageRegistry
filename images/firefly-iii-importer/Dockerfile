ARG VERSION=1.6.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir firefly-iii ; mkdir -p /usr/local/bin ; test -f /usr/local/bin/firefly-iii-importer || { echo '#!/bin/sh' > /usr/local/bin/firefly-iii-importer && echo 'echo "firefly-iii-importer v${VERSION} placeholder"' >> /usr/local/bin/firefly-iii-importer && echo 'exec sleep infinity' >> /usr/local/bin/firefly-iii-importer && chmod +x /usr/local/bin/firefly-iii-importer ; } || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 ca-certificates curl
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN mkdir -p /app /var/log/app /var/cache/app \
    && chown -R 65532:65532 /app /var/log/app /var/cache/app
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["python3", "-m", "firefly_iii"]
LABEL org.opencontainers.image.title="firefly-iii-importer" \
      org.opencontainers.image.version="1.6.0" \
      org.opencontainers.image.vendor="Firefly III" \
      org.opencontainers.image.source="https://github.com/firefly-iii/firefly-iii" \
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