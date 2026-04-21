# =============================================================================
# SOVEREIGN HARDENED GRAFANA-TOOLKIT
# Generated from template - Version: 10.4.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Node.js CLI tool requires runtime - cannot use scratch
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=10.4.1
ARG BUILD_DATE
ARG NODE_MAJOR=20

FROM debian:bookworm-20240101-slim AS downloader
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        gnupg && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL "https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key" | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" > /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

FROM debian:bookworm-20240101-slim
RUN groupadd -g 65534 toolkit && \
    useradd -m -u 65534 -g toolkit -s /usr/sbin/nologin toolkit
COPY --from=downloader /usr/bin/node /usr/local/bin/node
COPY --from=downloader /usr/lib/node_modules /usr/local/lib/node_modules
COPY --from=downloader /usr/bin/npm /usr/local/bin/npm
COPY --from=downloader /usr/bin/npx /usr/local/bin/npx
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN npm install -g @grafana/toolkit@${VERSION} && \
    strip /usr/local/bin/node 2>/dev/null || true && \
    mkdir -p /app/src /app/logs && \
    chown -R toolkit:toolkit /app /usr/local/lib/node_modules
USER 65534:65534
WORKDIR /app
ENV GRAFANA_TOOLKIT_VERSION=${VERSION} \
    NODE_ENV=production
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/usr/local/bin/node", "--version"]
ENTRYPOINT ["/usr/local/bin/npx", "grafana-toolkit"]
LABEL org.opencontainers.image.title="grafana-toolkit" \
      org.opencontainers.image.version="10.4.1" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.description="Grafana plugin toolkit CLI for building and testing plugins" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
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
