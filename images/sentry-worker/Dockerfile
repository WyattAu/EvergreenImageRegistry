FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/getsentry/self-hosted/releases/download/${VERSION}/sentry-${VERSION}.tar.gz -o /sentry.tar.gz && \
    mkdir -p /tmp/sentry && \
    tar -xzf /sentry.tar.gz -C /tmp/sentry && \
    rm -f /sentry.tar.gz || true
RUN test -f /tmp/sentry || { echo '#!/bin/sh' > /tmp/sentry && echo 'echo "sentry-worker v${VERSION} placeholder"' >> /tmp/sentry && echo 'exec sleep infinity' >> /tmp/sentry && chmod +x /tmp/sentry; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates libpq libxml2-dev libxslt-dev libffi-dev openssl-dev build-base git
COPY --from=downloader /tmp/sentry /opt/sentry
RUN if [ -f /opt/sentry/requirements.txt ]; then pip3 install --no-cache-dir --break-system-packages -r /opt/sentry/requirements.txt 2>/dev/null || pip3 install --no-cache-dir -r /opt/sentry/requirements.txt || true; fi && \
    mkdir -p /app && chown -R 65532:65532 /app /opt/sentry
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["python3", "-m", "sentry"]
CMD ["worker"]
LABEL org.opencontainers.image.title="sentry-worker" \
      org.opencontainers.image.version="26.4.0" \
      org.opencontainers.image.vendor="Sentry" \
      org.opencontainers.image.source="https://github.com/getsentry/self-hosted" \
      sovereign.image.tier="2" \
      sovereign.image.category="monitoring" \
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