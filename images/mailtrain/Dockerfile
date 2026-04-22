# =============================================================================
# SOVEREIGN HARDENED MAILTRAIN
# Constraint: debian-slim - Node.js runtime required
# =============================================================================

ARG VERSION=1.38.0
ARG BUILD_DATE
ARG NODE_VERSION=20

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends         curl="7.88.1-*"         ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://deb.nodesource.com/setup_${NODE_VERSION}.x" | bash - &&     apt-get update &&     apt-get install -y --no-install-recommends nodejs &&     rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN curl -fsSL "https://github.com/Mailtrain/mailtrain/archive/refs/tags/v${VERSION}.tar.gz" -o /tmp/mailtrain.tar.gz && \
    tar -xzf /tmp/mailtrain.tar.gz -C /build --strip-components=1 && \
    rm /tmp/mailtrain.tar.gz && \
    npm install --omit=dev 2>/dev/null || true

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends         curl="7.88.1-*"         ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://deb.nodesource.com/setup_${NODE_VERSION}.x" | bash - &&     apt-get update &&     apt-get install -y --no-install-recommends nodejs &&     rm -rf /var/lib/apt/lists/*
RUN groupadd -r -g 65534 appuser && useradd -r -u 65534 -g appuser -d /app -s /usr/sbin/nologin appuser
WORKDIR /app
COPY --from=builder /build/dist /app/dist
COPY --from=builder /build/node_modules /app/node_modules
COPY --from=builder /build/package.json /app/
RUN chown -R 65534:65534 /app
USER 65534:65534
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["curl", "-sf", "http://localhost:3000/health"]
ENTRYPOINT [["node", "/app/server.js"]]
LABEL org.opencontainers.image.title="mailtrain"       org.opencontainers.image.description="Mailtrain - self-hosted newsletter and mailing list manager"       org.opencontainers.image.version="1.38.0"       org.opencontainers.image.vendor="Mailtrain"       org.opencontainers.image.source="https://github.com/Mailtrain/mailtrain"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian-slim="true"
