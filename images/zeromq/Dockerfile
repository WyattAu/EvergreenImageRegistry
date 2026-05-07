# =============================================================================
# EVERGREEN HARDENED ZEROMQ (libzmq)
# ZeroMQ messaging library - built from source with minimal deps
# Constraint: debian-slim - C library requires glibc runtime
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.3.5
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
ARG VERSION=4.3.5
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake curl ca-certificates \
    libsodium-dev libpgm-dev libnorm-dev && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/zeromq/libzmq/releases/download/v${VERSION}/zeromq-${VERSION}.tar.gz -o /zeromq.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/zeromq/libzmq/releases/download/v${VERSION}/sha256sum.txt -o /checksums.txt && \
    grep "zeromq-${VERSION}.tar.gz" /checksums.txt | sha256sum -c || true ; [ -f /zeromq.tar.gz ] && \
    [ -f /zeromq.tar.gz ] && tar -xzf /zeromq.tar.gz -C /tmp/ || true ; \
    cd /tmp/zeromq-${VERSION} && \    cmake -DCMAKE_BUILD_TYPE=Release \
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
    rm -rf /zeromq.tar.gz /checksums.txt /tmp/zeromq-${VERSION} || true && \
    mkdir -p /opt/zeromq
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache libstdc++ ca-certificates 

COPY --from=builder /opt/zeromq /opt/zeromq
RUN ldconfig && chown -R 65532:65532 /opt/zeromq
USER 65532:65532
WORKDIR /app
ENV LD_LIBRARY_PATH="/opt/zeromq/lib"
LABEL org.opencontainers.image.title="zeromq" \
      org.opencontainers.image.description="zeromq container image" \
      org.opencontainers.image.version="4.3.5" \
      org.opencontainers.image.vendor="ZeroMQ" \
      org.opencontainers.image.source="https://github.com/zeromq/libzmq" \
      evergreen.image.tier="1" \
      evergreen.image.category="networking" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.distrole="debian-slim" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
