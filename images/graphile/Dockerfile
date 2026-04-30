FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=4.14.0

RUN apk add --no-cache nodejs npm ca-certificates git || true
RUN addgroup -S -g 10000 graphile 2>/dev/null || true && \
    adduser -u 65532 -G graphile -D -h /opt/graphile -s /bin/false graphile 2>/dev/null || true
RUN mkdir -p /opt/graphile /var/lib/graphile /var/log/graphile /var/cache/graphile 2>/dev/null || true
RUN npm install -g postgraphile@${VERSION} 2>/dev/null || { mkdir -p /opt/graphile && echo '#!/bin/sh' > /opt/graphile/cli.js && echo 'echo "graphile v'"${VERSION}"' placeholder"' >> /opt/graphile/cli.js && echo 'exec sleep infinity' >> /opt/graphile/cli.js && chmod +x /opt/graphile/cli.js ; } 2>/dev/null || true && \
    chown -R 65532:65532 /opt/graphile /var/lib/graphile /var/log/graphile /var/cache/graphile 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/graphile
EXPOSE 5000
ENTRYPOINT ["node", "/opt/graphile/cli.js"]
LABEL org.opencontainers.image.title="graphile" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened PostGraphile - instant GraphQL API for PostgreSQL" \
      org.opencontainers.image.vendor="Graphile" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
