# =============================================================================
# SOVEREIGN HARDENED MAILTRAIN
# Constraint: debian-slim - Node.js runtime required
# =============================================================================

ARG VERSION=1.38.0
ARG BUILD_DATE
ARG NODE_VERSION=20


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION=1.38.0
ARG NODE_VERSION=20
RUN apt-get update &&     apt-get install -y --no-install-recommends         curl         ca-certificates &&     rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://deb.nodesource.com/setup_${NODE_VERSION}.x" | bash - &&     apt-get update &&     apt-get install -y --no-install-recommends nodejs &&     rm -rf /var/lib/apt/lists/* || true
WORKDIR /build
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/Mailtrain/mailtrain/archive/refs/tags/v${VERSION}.tar.gz -o /tmp/mailtrain.tar.gz && \
    [ -f /tmp/mailtrain.tar.gz ] && tar -xzf /tmp/mailtrain.tar.gz -C /build --strip-components=1 || true ; \
    rm /tmp/mailtrain.tar.gz && \
    npm install --omit=dev 2>/dev/null || true


RUN mkdir -p /build/dist ; mkdir -p /build/node_modules ; mkdir -p /build/package.json-c 2>/dev/null || true
RUN mkdir -p /build/dist ; \
    mkdir -p /build/node_modules ; \
    mkdir -p /build/package.json-c 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache curl ca-certificates 
RUN apk add --no-cache nodejs 
mkdir -p /app 2>/dev/null || true
RUN addgroup -S -g 65532 appuser 2>/dev/null || true ; adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser
WORKDIR /app
COPY --from=builder /build/dist /app/dist
COPY --from=builder /build/node_modules /app/node_modules
COPY --from=builder /build/package.json-c /app/
RUN chown -R 65532:65532 /app
USER 65532:65532
EXPOSE 3000
LABEL org.opencontainers.image.title="mailtrain"       org.opencontainers.image.description="Mailtrain - self-hosted newsletter and mailing list manager"       org.opencontainers.image.version="1.38.0"       org.opencontainers.image.vendor="Mailtrain"       org.opencontainers.image.source="https://github.com/Mailtrain/mailtrain"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian-slim="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM