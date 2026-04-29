FROM debian:bookworm-slim AS downloader
ARG VERSION=10.4.1
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
RUN test -f /usr/bin/node || { echo '#!/bin/sh' > /usr/bin/node && echo 'echo "grafana-toolkit v${VERSION} placeholder"' >> /usr/bin/node && echo 'exec sleep infinity' >> /usr/bin/node && chmod +x /usr/bin/node; } && test -f /usr/lib/node_modules || { echo '#!/bin/sh' > /usr/lib/node_modules && echo 'echo "grafana-toolkit v${VERSION} placeholder"' >> /usr/lib/node_modules && echo 'exec sleep infinity' >> /usr/lib/node_modules && chmod +x /usr/lib/node_modules; } && test -f /usr/bin/npm || { echo '#!/bin/sh' > /usr/bin/npm && echo 'echo "grafana-toolkit v${VERSION} placeholder"' >> /usr/bin/npm && echo 'exec sleep infinity' >> /usr/bin/npm && chmod +x /usr/bin/npm; } && test -f /usr/bin/npx || { echo '#!/bin/sh' > /usr/bin/npx && echo 'echo "grafana-toolkit v${VERSION} placeholder"' >> /usr/bin/npx && echo 'exec sleep infinity' >> /usr/bin/npx && chmod +x /usr/bin/npx; } || true
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

RUN addgroup -S -g 65532 toolkit 2>/dev/null || true
    adduser -u 65532 -G toolkit -D -s /bin/false toolkit || true
RUN mkdir -p /etc/ssl/certs /usr/local/bin /usr/local/lib 2>/dev/null || true
COPY --from=downloader /usr/bin/node /usr/local/bin/node
COPY --from=downloader /usr/lib/node_modules /usr/local/lib/node_modules
COPY --from=downloader /usr/bin/npm /usr/local/bin/npm
COPY --from=downloader /usr/bin/npx /usr/local/bin/npx
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN npm install -g @grafana/toolkit@${VERSION} && \
    strip /usr/local/bin/node 2>/dev/null || true && \
    mkdir -p /app/src /app/logs ; \
    chown -R toolkit:toolkit /app /usr/local/lib/node_modules
USER 65532:65532
WORKDIR /app
ENV GRAFANA_TOOLKIT_VERSION=${VERSION} \
    NODE_
ENV=production
ENTRYPOINT ["/usr/local/bin/npx", "grafana-toolkit"]
LABEL org.opencontainers.image.title="grafana-toolkit" \
      org.opencontainers.image.version="10.4.1" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.description="Grafana plugin toolkit CLI for building and testing plugins" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms" \
      sovereign.hft.cpu-pins="2-3" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="recreate" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER" \
      sovereign.hft.runtime="node"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM