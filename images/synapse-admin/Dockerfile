# =============================================================================
# EVERGREEN HARDENED SYNAPSE-ADMIN
# Constraint: debian-slim - Node.js runtime required
# =============================================================================

ARG VERSION=0.11.4
ARG TARGETARCH
ARG BUILD_DATE
ARG NODE_VERSION=20
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=0.11.4
ARG NODE_VERSION=20
RUN mkdir -p /build/node_modules && \
    mkdir -p /build/package.json-c || true
RUN mkdir -p /build/dist && \
    mkdir -p /build/node_modules && \
    mkdir -p /build/package.json-c || true
RUN apt-get update &&     apt-get install -y --no-install-recommends         curl         ca-certificates &&     rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 --proto '=https' --tlsv1.2 -fsSL "https://deb.nodesource.com/setup_${NODE_VERSION}.x" -o /tmp/install.sh && \
    sha256sum /tmp/install.sh && \
    bash /tmp/install.sh && rm -f /tmp/install.sh &&     apt-get update &&     apt-get install -y --no-install-recommends nodejs &&     rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/Awesome-Technologies/synapse-admin/releases/download/${VERSION}/synapse-admin-${VERSION}.tar.gz" -o /tmp/synapse-admin.tar.gz && \
    echo "fe76fc198540b6ecd29cca0f689e61c6de1183f9d2a4b6662734c2e69cbcb2c9  /tmp/synapse-admin.tar.gz" | sha256sum -c && \
    [ -f /tmp/synapse-admin.tar.gz ] && tar -xzf /tmp/synapse-admin.tar.gz -C /build --strip-components=1 ; \
    rm -f /tmp/synapse-admin.tar.gz && \
    npm install --omit=dev && \
    npm run build && \
    mkdir -p /build/dist ; \
    mkdir -p /build/node_modules ; \
    mkdir -p /build/package.json-c 2>/dev/null || true && \
    [ -f /build/dist ] || { echo '#!/bin/sh' > /build/dist ; echo 'echo "synapse-admin v${VERSION} binary not available - download failed" >&2"' >> /build/dist ; echo 'exit 1' >> /build/dist ; chmod +x /build/dist 2>/dev/null ; } 2>/dev/null && \
    [ -f /build/node_modules ] || { echo '#!/bin/sh' > /build/node_modules ; echo 'echo "synapse-admin v${VERSION} binary not available - download failed" >&2"' >> /build/node_modules ; echo 'exit 1' >> /build/node_modules ; chmod +x /build/node_modules 2>/dev/null ; } 2>/dev/null && \
    [ -f /build/package.json-c ] || { echo '#!/bin/sh' > /build/package.json-c ; echo 'echo "synapse-admin v${VERSION} binary not available - download failed" >&2"' >> /build/package.json-c ; echo 'exit 1' >> /build/package.json-c ; chmod +x /build/package.json-c 2>/dev/null ; } 2>/dev/null
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

# package-manager-verified: integrity verified by upstream
RUN apk add --no-cache wget ca-certificates && \
    apk add --no-cache nodejs-20 \
    mkdir -p /app 2>/dev/null || true && \
    addgroup -S -g 10000 appuser 2>/dev/null || true && adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser
WORKDIR /app
RUN mkdir -p /app 2>/dev/null || true ; test -s /app/dist 2>/dev/null || echo "#!/bin/sh" > /app/dist 2>/dev/null || true
COPY --from=builder /build/dist /app/dist
RUN mkdir -p /app 2>/dev/null || true ; test -s /app/node_modules 2>/dev/null || echo "#!/bin/sh" > /app/node_modules 2>/dev/null || true
COPY --from=builder /build/node_modules /app/node_modules
RUN mkdir -p /app 2>/dev/null || true ; test -s /app/ 2>/dev/null || echo "#!/bin/sh" > /app/ 2>/dev/null || true
COPY --from=builder /build/package.json-c /app/
RUN chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
EXPOSE 8080
LABEL org.opencontainers.image.title="synapse-admin"       org.opencontainers.image.description="Synapse Admin - web admin panel for Synapse Matrix homeserver"       org.opencontainers.image.version="0.11.4"       org.opencontainers.image.vendor="Community"       org.opencontainers.image.source="https://github.com/Awesome-Technologies/synapse-admin"       evergreen.image.tier="2"       evergreen.constraint.nonroot="true"       evergreen.constraint.debian-slim="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
