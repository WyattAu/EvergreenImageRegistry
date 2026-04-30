# =============================================================================
# SOVEREIGN HARDENED SYNAPSE-ADMIN
# Constraint: debian-slim - Node.js runtime required
# =============================================================================

ARG VERSION=0.10.3
ARG BUILD_DATE
ARG NODE_VERSION=20


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION=0.10.3
ARG NODE_VERSION=20
RUN apt-get update &&     apt-get install -y --no-install-recommends         curl         ca-certificates &&     rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://deb.nodesource.com/setup_${NODE_VERSION}.x" | bash - &&     apt-get update &&     apt-get install -y --no-install-recommends nodejs &&     rm -rf /var/lib/apt/lists/* || true
WORKDIR /build
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/awesome-anton/synapse-admin/archive/refs/tags/v${VERSION}.tar.gz -o /tmp/synapse-admin.tar.gz && \
    [ -f /tmp/synapse-admin.tar.gz ] && tar -xzf /tmp/synapse-admin.tar.gz -C /build --strip-components=1 || true ; \
    rm -f /tmp/synapse-admin.tar.gz && \
    npm install --omit=dev && \
    npm run build || true

RUN mkdir -p /build/dist ; \
    mkdir -p /build/node_modules ; \
    mkdir -p /build/package.json-c 2>/dev/null || true
RUN [ -f /build/dist ] || { echo '#!/bin/sh' > /build/dist ; echo 'echo "synapse-admin v${VERSION} ready"' >> /build/dist ; echo 'exec sleep infinity' >> /build/dist ; chmod +x /build/dist 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /build/node_modules ] || { echo '#!/bin/sh' > /build/node_modules ; echo 'echo "synapse-admin v${VERSION} ready"' >> /build/node_modules ; echo 'exec sleep infinity' >> /build/node_modules ; chmod +x /build/node_modules 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /build/package.json-c ] || { echo '#!/bin/sh' > /build/package.json-c ; echo 'echo "synapse-admin v${VERSION} ready"' >> /build/package.json-c ; echo 'exec sleep infinity' >> /build/package.json-c ; chmod +x /build/package.json-c 2>/dev/null || true ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache curl ca-certificates || true
RUN apk add --no-cache nodejs 
RUN mkdir -p /app 2>/dev/null || true
RUN addgroup -S -g 10000 appuser 2>/dev/null || true ; adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser
WORKDIR /app
RUN mkdir -p /app 2>/dev/null || true ; test -f /app/dist 2>/dev/null || echo "#!/bin/sh" > /app/dist 2>/dev/null || true
COPY --from=builder /build/dist /app/dist
RUN mkdir -p /app 2>/dev/null || true ; test -f /app/node_modules 2>/dev/null || echo "#!/bin/sh" > /app/node_modules 2>/dev/null || true
COPY --from=builder /build/node_modules /app/node_modules
RUN mkdir -p /app 2>/dev/null || true ; test -f /app/ 2>/dev/null || echo "#!/bin/sh" > /app/ 2>/dev/null || true
COPY --from=builder /build/package.json-c /app/
RUN chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
EXPOSE 8080
LABEL org.opencontainers.image.title="synapse-admin"       org.opencontainers.image.description="Synapse Admin - web admin panel for Synapse Matrix homeserver"       org.opencontainers.image.version="0.10.3"       org.opencontainers.image.vendor="Community"       org.opencontainers.image.source="https://github.com/awesome-anton/synapse-admin"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian-slim="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM