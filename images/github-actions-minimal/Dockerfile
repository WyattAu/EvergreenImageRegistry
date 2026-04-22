# =============================================================================
# SOVEREIGN HARDENED GITHUB-ACTIONS-MINIMAL
# Constraint: debian-slim - Node.js runtime required
# =============================================================================

ARG VERSION=2.321.0
ARG BUILD_DATE
ARG NODE_VERSION=20

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends         curl="7.88.1-*"         ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://deb.nodesource.com/setup_${NODE_VERSION}.x" | bash - &&     apt-get update &&     apt-get install -y --no-install-recommends nodejs &&     rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN curl -fsSL "https://github.com/actions/runner/releases/download/v${VERSION}/actions-runner-linux-x64-${VERSION}.tar.gz" -o /tmp/runner.tar.gz && \
    tar -xzf /tmp/runner.tar.gz -C /build && \
    rm /tmp/runner.tar.gz && \
    chown -R root:root /build

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
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["curl", "-sf", "http://localhost:8080/health"]
ENTRYPOINT [["/build/run.sh"]]
LABEL org.opencontainers.image.title="github-actions-minimal"       org.opencontainers.image.description="GitHub Actions Minimal Runner - lightweight self-hosted runner"       org.opencontainers.image.version="2.321.0"       org.opencontainers.image.vendor="GitHub"       org.opencontainers.image.source="https://github.com/actions/runner"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian-slim="true"
