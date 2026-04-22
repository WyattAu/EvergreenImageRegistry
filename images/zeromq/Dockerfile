# =============================================================================
# SOVEREIGN HARDENED ZEROMQ (libzmq)
# ZeroMQ messaging library - built from source with minimal deps
# Constraint: debian-slim - C library requires glibc runtime
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.3.5
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-base cmake curl ca-certificates \
    libsodium-dev libpgm-dev libnorm-dev && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/zeromq/libzmq/releases/download/v${VERSION}/zeromq-${VERSION}.tar.gz" -o /zeromq.tar.gz && \
    curl -fsSL "https://github.com/zeromq/libzmq/releases/download/v${VERSION}/sha256sum.txt" -o /checksums.txt && \
    grep "zeromq-${VERSION}.tar.gz" /checksums.txt | sha256sum -c - && \
    tar -xzf /zeromq.tar.gz -C /tmp/ && \
    cd /tmp/zeromq-${VERSION} && \
    cmake -DCMAKE_BUILD_TYPE=Release \
          -DCMAKE_INSTALL_PREFIX=/opt/zeromq \
          -DWITH_DOC=OFF \
          -DWITH_TESTS=OFF \
          -DENABLE_DRAFTS=OFF \
          -DBUILD_STATIC=ON \
          -DBUILD_SHARED=ON \
          . && \
    cmake --build . -j"$(nproc)" && \
    cmake --install . && \
    strip --strip-unneeded /opt/zeromq/lib/libzmq.so.5.2.5 && \
    strip --strip-unneeded /opt/zeromq/lib/libzmq.a && \
    rm -rf /zeromq.tar.gz /checksums.txt /tmp/zeromq-${VERSION}

# hadolint ignore=DL3023
FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache libstdc++ ca-certificates

COPY --from=builder /opt/zeromq /opt/zeromq
RUN ldconfig && chown -R 65532:65532 /opt/zeromq

USER 65532:65532
WORKDIR /app
ENV LD_LIBRARY_PATH="/opt/zeromq/lib"
LABEL org.opencontainers.image.title="zeromq" \
      org.opencontainers.image.version="4.3.5" \
      org.opencontainers.image.vendor="ZeroMQ" \
      org.opencontainers.image.source="https://github.com/zeromq/libzmq" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distrole="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
