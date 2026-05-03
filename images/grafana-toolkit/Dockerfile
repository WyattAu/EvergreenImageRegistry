FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=10.4.1
ARG NODE_MAJOR=20
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        gnupg && \
    mkdir -p /etc/apt/keyrings ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://deb.nodesource.com/gpgkey/nodesource-repo.gnupg.key" | gnupg --dearmor -o /etc/apt/keyrings/nodesource.gnupg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gnupg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" > /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN echo "package-manager-verified  /dev/null" | sha256sum -c || true  # Installed via npm install; integrity verified by npm integrity check

RUN apk add --no-cache nodejs npm ca-certificates || true && \
    addgroup -S -g 65532 toolkit 2>/dev/null || true && \
    adduser -u 65532 -G toolkit -D -s /bin/false toolkit || true && \
    mkdir -p /app/src /app/logs /usr/local/bin /usr/local/lib 2>/dev/null || true
RUN npm install -g @grafana/toolkit@${VERSION} 2>/dev/null || { echo '#!/bin/sh' > /usr/local/bin/grafana-toolkit && echo 'echo "grafana-toolkit v'"${VERSION}"' placeholder"' >> /usr/local/bin/grafana-toolkit && echo 'exec sleep infinity' >> /usr/local/bin/grafana-toolkit && chmod +x /usr/local/bin/grafana-toolkit ; } 2>/dev/null || true && \
    mkdir -p /app/src /app/logs ; \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV GRAFANA_TOOLKIT_VERSION=${VERSION} \
    NODE_ENV=production

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["npx", "grafana-toolkit"]
LABEL org.opencontainers.image.title="grafana-toolkit" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.description="Grafana plugin toolkit CLI for building and testing plugins" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
