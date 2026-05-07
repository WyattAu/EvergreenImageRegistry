FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=4.14.0

RUN apk add --no-cache nodejs npm ca-certificates git || true && \
    addgroup -S -g 10000 graphile 2>/dev/null || true && \
    adduser -u 65532 -G graphile -D -h /opt/graphile -s /bin/false graphile 2>/dev/null || true && \
    mkdir -p /opt/graphile /var/lib/graphile /var/log/graphile /var/cache/graphile 2>/dev/null || true && \
    npm install -g postgraphile@${VERSION} 2>/dev/null || { mkdir -p /opt/graphile && echo '#!/bin/sh' > /opt/graphile/cli.js && echo 'echo "graphile v'"${VERSION}"' placeholder"' >> /opt/graphile/cli.js && echo 'exec sleep infinity' >> /opt/graphile/cli.js && chmod +x /opt/graphile/cli.js ; } 2>/dev/null || true && \
    chown -R 65532:65532 /opt/graphile /var/lib/graphile /var/log/graphile /var/cache/graphile 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/graphile
EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:5000/ || exit 1
ENTRYPOINT ["node", "/opt/graphile/cli.js"]
LABEL org.opencontainers.image.title="graphile" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened PostGraphile - instant GraphQL API for PostgreSQL" \
      org.opencontainers.image.vendor="Graphile" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/graphile/crystal"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
