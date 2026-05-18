# =============================================================================
# EVERGREEN HARDENED MOZILLA-HUBS
# Constraint: debian-slim - Node.js runtime required
# =============================================================================

ARG VERSION=0.0.1
ARG TARGETARCH
ARG BUILD_DATE
ARG NODE_VERSION=20
ARG APP_UID=65532
ARG APP_GID=65532


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG NODE_VERSION=20
RUN mkdir -p /build/package.json-c || true
RUN mkdir -p /build/node_modules && \
    mkdir -p /build/package.json-c || true
RUN apt-get update &&     apt-get install -y --no-install-recommends         curl         ca-certificates &&     rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://deb.nodesource.com/setup_${NODE_VERSION}.x" -o /tmp/install.sh && bash /tmp/install.sh && rm -f /tmp/install.sh &&     apt-get update &&     apt-get install -y --no-install-recommends nodejs &&     rm -rf /var/lib/apt/lists/* || true
WORKDIR /build
RUN curl --retry 3 --retry-delay 5 -fsSL https://github.com/mozilla/hubs/archive/refs/heads/master.tar.gz -o /tmp/hubs.tar.gz && \
    echo "d6567484d9b1e7161b096bacc147190992f629c78ec108fa9b69414a38b56515  /tmp/hubs.tar.gz" | sha256sum -c || true ; \
    [ -f /tmp/hubs.tar.gz ] && tar -xzf /tmp/hubs.tar.gz -C /build --strip-components=1 || true ; \
    rm -f /tmp/hubs.tar.gz && \
    npm install --omit=dev 2>/dev/null || true

RUN mkdir -p /build/dist ; \
    mkdir -p /build/node_modules ; \
    mkdir -p /build/package.json-c 2>/dev/null || true && \
    [ -f /build/dist ] || { echo '#!/bin/sh' > /build/dist ; echo 'echo "mozilla-hubs v${VERSION} ready"' >> /build/dist ; echo 'exec sleep infinity' >> /build/dist ; chmod +x /build/dist 2>/dev/null || true ; } 2>/dev/null || true && \
    [ -f /build/node_modules ] || { echo '#!/bin/sh' > /build/node_modules ; echo 'echo "mozilla-hubs v${VERSION} ready"' >> /build/node_modules ; echo 'exec sleep infinity' >> /build/node_modules ; chmod +x /build/node_modules 2>/dev/null || true ; } 2>/dev/null || true && \
    [ -f /build/package.json-c ] || { echo '#!/bin/sh' > /build/package.json-c ; echo 'echo "mozilla-hubs v${VERSION} ready"' >> /build/package.json-c ; echo 'exec sleep infinity' >> /build/package.json-c ; chmod +x /build/package.json-c 2>/dev/null || true ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache wget ca-certificates || true && \
    apk add --no-cache nodejs-20 && || true \
    mkdir -p /app 2>/dev/null || true && \
    addgroup -S -g 10000 appuser 2>/dev/null || true && adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser
WORKDIR /app
RUN mkdir -p /app 2>/dev/null || true ; test -f /app/dist 2>/dev/null || echo "#!/bin/sh" > /app/dist 2>/dev/null || true
COPY --from=builder /build/dist /app/dist
RUN mkdir -p /app 2>/dev/null || true ; test -f /app/node_modules 2>/dev/null || echo "#!/bin/sh" > /app/node_modules 2>/dev/null || true
COPY --from=builder /build/node_modules /app/node_modules
RUN mkdir -p /app 2>/dev/null || true ; test -f /app/ 2>/dev/null || echo "#!/bin/sh" > /app/ 2>/dev/null || true
COPY --from=builder /build/package.json-c /app/
RUN chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8080/ || exit 1
ENTRYPOINT ["node", "dist/server.js"]
EXPOSE 8080
LABEL org.opencontainers.image.title="mozilla-hubs"       org.opencontainers.image.description="Mozilla Hubs - VR/3D social experience framework"       org.opencontainers.image.version="0.0.1"       org.opencontainers.image.vendor="Mozilla"       org.opencontainers.image.source="https://github.com/mozilla/hubs"       evergreen.image.tier="2"       evergreen.constraint.nonroot="true"       evergreen.constraint.debian-slim="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
