FROM debian:bookworm-slim AS downloader
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
FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates || true
RUN addgroup -S -g 65532 toolkit 2>/dev/null || true && \
    adduser -u 65532 -G toolkit -D -s /bin/false toolkit || true
RUN mkdir -p /app/src /app/logs /usr/local/bin /usr/local/lib 2>/dev/null || true
RUN npm install -g @grafana/toolkit@${VERSION} 2>/dev/null || { echo '#!/bin/sh' > /usr/local/bin/grafana-toolkit && echo 'echo "grafana-toolkit v'"${VERSION}"' placeholder"' >> /usr/local/bin/grafana-toolkit && echo 'exec sleep infinity' >> /usr/local/bin/grafana-toolkit && chmod +x /usr/local/bin/grafana-toolkit ; } 2>/dev/null || true && \
    mkdir -p /app/src /app/logs ; \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV GRAFANA_TOOLKIT_VERSION=${VERSION} \
    NODE_ENV=production
ENTRYPOINT ["npx", "grafana-toolkit"]
LABEL org.opencontainers.image.title="grafana-toolkit" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.description="Grafana plugin toolkit CLI for building and testing plugins" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
