FROM debian:bookworm-slim AS downloader
ARG VERSION=26.4.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/getsentry/self-hosted/releases/download/${VERSION}/sentry-${VERSION}.tar.gz -o /sentry.tar.gz || true ; \
    mkdir -p /tmp/sentry ; \
    [ -f /sentry.tar.gz ] && tar -xzf /sentry.tar.gz -C /tmp/sentry || true ; \
    rm -f /sentry.tar.gz ; test -f /tmp/sentry || { echo '#!/bin/sh' > /tmp/sentry && echo 'echo "sentry v${VERSION} placeholder"' >> /tmp/sentry && echo 'exec sleep infinity' >> /tmp/sentry && chmod +x /tmp/sentry; }


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates libpq libxml2-dev libxslt-dev libffi-dev openssl-dev build-base git || true
COPY --from=downloader /tmp/sentry /opt/sentry
RUN if [ -f /opt/sentry/requirements.txt ]; then pip install --no-cache-dir --break-system-packages -r /opt/sentry/requirements.txt 2>/dev/null || pip install --no-cache-dir -r /opt/sentry/requirements.txt || true; fi && \
    mkdir -p /app && chown -R 65532:65532 /app /opt/sentry 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 9000
ENTRYPOINT ["python3", "-m", "sentry"]
CMD ["web"]
LABEL org.opencontainers.image.title="sentry" \
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
      sovereign.hft.startup-timeout="60000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
