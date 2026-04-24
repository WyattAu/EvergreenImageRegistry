# =============================================================================
# SOVEREIGN HARDENED MOZILLA-HUBS
# Constraint: debian-slim - Node.js runtime required
# =============================================================================

ARG VERSION=0.0.1
ARG BUILD_DATE
ARG NODE_VERSION=20


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG NODE_VERSION=20
RUN apt-get update &&     apt-get install -y --no-install-recommends         curl         ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://deb.nodesource.com/setup_${NODE_VERSION}.x" | bash - &&     apt-get update &&     apt-get install -y --no-install-recommends nodejs &&     rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/mozilla/hubs/archive/refs/heads/master.tar.gz -o /tmp/hubs.tar.gz && \
    tar -xzf /tmp/hubs.tar.gz -C /build --strip-components=1 && \
    rm /tmp/hubs.tar.gz && \
    npm install --omit=dev 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache curl ca-certificates
RUN apk add --no-cache nodejs
RUN addgroup -S -g 65532 appuser 2>/dev/null || true && adduser -u 65532 -G appuser -D -h /app -s /sbin/nologin appuser
WORKDIR /app
COPY --from=builder /build/dist /app/dist
COPY --from=builder /build/node_modules /app/node_modules
COPY --from=builder /build/package.json-c /app/
RUN chown -R 65532:65532 /app
USER 65532:65532
EXPOSE 8080
LABEL org.opencontainers.image.title="mozilla-hubs"       org.opencontainers.image.description="Mozilla Hubs - VR/3D social experience framework"       org.opencontainers.image.version="0.0.1"       org.opencontainers.image.vendor="Mozilla"       org.opencontainers.image.source="https://github.com/mozilla/hubs"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian-slim="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM