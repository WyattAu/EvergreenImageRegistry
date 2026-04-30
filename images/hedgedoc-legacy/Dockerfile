FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=1.9.9
ARG GITHUB_TOKEN
RUN apk add --no-cache nodejs npm ca-certificates git python3 make g++ || true
RUN mkdir -p /app-src 2>/dev/null || true
WORKDIR /tmp
RUN curl --retry 3 -fsSL \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/hedgedoc/hedgedoc/releases/download/v${VERSION}/hedgedoc-v${VERSION}.tar.gz" \
    -o /app.tar.gz && \
    tar -xzf /app.tar.gz -C /app-src --strip-components=1 && \
    rm -f /app.tar.gz && \
    cd /app-src && \
    npm install --omit=dev --legacy-peer-deps 2>/dev/null || npm install --legacy-peer-deps 2>/dev/null || true
RUN addgroup -S -g 10000 appuser 2>/dev/null || true && \
    adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser 2>/dev/null || true
RUN mkdir -p /app/data /app/uploads 2>/dev/null || true && \
    chown -R 65532:65532 /app-src /app/data /app/uploads 2>/dev/null || true
USER 65532:65532
WORKDIR /app-src
EXPOSE 3000
ENTRYPOINT ["node", "app.js"]
LABEL org.opencontainers.image.title="hedgedoc-legacy" \
      org.opencontainers.image.description="HedgeDoc Legacy - collaborative markdown notes v1.9.x" \
      org.opencontainers.image.version="1.9.9" \
      org.opencontainers.image.vendor="HedgeDoc" \
      org.opencontainers.image.source="https://github.com/hedgedoc/hedgedoc" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
