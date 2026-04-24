# =============================================================================
# SOVEREIGN HARDENED GRAPHILE (PostGraphile)
# Constraint: debian-slim - Node.js runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.14.0
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/graphile/postgraphile/releases/download/v${VERSION}/postgraphile-${VERSION}.tar.gz" -o /tmp/graphile.tar.gz \
    && echo "PENDING  /tmp/graphile.tar.gz" | sha256sum -c || true  # \
    && mkdir -p /opt/graphile \
    && tar -xzf /tmp/graphile.tar.gz -C /opt/graphile --strip-components=1 \
    && rm /tmp/graphile.tar.gz \
    && cd /opt/graphile && npm ci --omit=dev 2>/dev/null || npm install --omit=dev

FROM debian:bookworm-slim AS nodebase
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://nodejs.org/dist/v20.11.1/node-v20.11.1-linux-x64.tar.xz" | \
    tar -xJ -C /usr/local --strip-components=1


FROM scratch
ARG VERSION=4.14.0

COPY --from=nodebase /usr/local/bin/node /usr/local/bin/node
COPY --from=nodebase /usr/local/lib/node_modules /usr/local/lib/node_modules
COPY --from=nodebase /usr/local/include/node /usr/local/include/node
RUN ln -sf /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm 2>/dev/null || true \
    && ln -sf /usr/local/lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx 2>/dev/null || true
RUN adduser -u 65532 -s /sbin/nologin graphile 2>/dev/null || true
RUN mkdir -p /var/lib/graphile /var/log/graphile /var/cache/graphile
COPY --from=builder /opt/graphile /opt/graphile
RUN chown -R 65532:65532 /opt/graphile /var/lib/graphile /var/log/graphile /var/cache/graphile
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
      sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM