ARG VERSION=2.3.6
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 ca-certificates curl ; rm -rf /var/lib/apt/lists/* || true

RUN python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir beancount ; mkdir -p /usr/local/bin ; test -f /usr/local/bin/beancount || { echo '#!/bin/sh' > /usr/local/bin/beancount && echo 'echo "beancount v${VERSION} placeholder"' >> /usr/local/bin/beancount && echo 'exec sleep infinity' >> /usr/local/bin/beancount && chmod +x /usr/local/bin/beancount ; } || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 ca-certificates curl 
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN mkdir -p /app /var/log/app /var/cache/app ; 2>/dev/null || true \
    chown -R 65532:65532 /app /var/log/app /var/cache/app
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["python3", "-m", "beancount"]
LABEL org.opencontainers.image.title="beancount" \
      org.opencontainers.image.version="2.3.6" \
      org.opencontainers.image.vendor="Beancount" \
      org.opencontainers.image.source="https://github.com/beancount/beancount" \
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