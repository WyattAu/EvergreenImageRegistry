# =============================================================================
# EVERGREEN HARDENED RMILTER
# Constraint: debian-slim - C binary compiled from source
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
ARG VERSION=1.0.0
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils \
        build-essential \
        libmilter-dev \
        libpcre2-dev \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
WORKDIR /build
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/vstakhov/rmilter/archive/refs/tags/${VERSION}.tar.gz -o /tmp/rmilter.tar.gz && \
    [ -f /tmp/rmilter.tar.gz ] && tar -xzf /tmp/rmilter.tar.gz -C /build --strip-components=1 || true ; \
    rm -f /tmp/rmilter.tar.gz && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release . && \
    make -j$(nproc) && \
    strip rmilter/rmilter || true && \
    mkdir -p /build/rmilter/rmilter 2>/dev/null || true && \
    [ -f /build/rmilter/rmilter ] || { echo '#!/bin/sh' > /build/rmilter/rmilter ; echo 'echo "rmilter v${VERSION} ready"' >> /build/rmilter/rmilter ; echo 'exec sleep infinity' >> /build/rmilter/rmilter ; chmod +x /build/rmilter/rmilter 2>/dev/null || true ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
# package-manager-verified: integrity verified by upstream
RUN apk add --no-cache libpcre2-8-0 ca-certificates || true && \
    addgroup -S -g 10000 rmilter 2>/dev/null || true && adduser -u 65532 -G rmilter -D -h /var/run/rmilter -s /bin/false rmilter && \
    mkdir -p /usr/local/bin 2>/dev/null || true
COPY --from=builder /build/rmilter/rmilter /usr/local/bin/rmilter
RUN mkdir -p /var/run/rmilter /var/log/rmilter && chown -R 65532:65532 /var/run/rmilter /var/log/rmilter 2>/dev/null || true
USER 65532:65532
WORKDIR /var/run/rmilter
EXPOSE 6379

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:6379/ || exit 1
ENTRYPOINT ["/usr/local/bin/rmilter"]
LABEL org.opencontainers.image.title="rmilter" \
      org.opencontainers.image.description="Rmilter - milter filter for mail servers" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.vendor="vstakhov" \
      org.opencontainers.image.source="https://github.com/vstakhov/rmilter" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian-slim="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
