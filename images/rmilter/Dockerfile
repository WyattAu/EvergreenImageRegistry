# =============================================================================
# SOVEREIGN HARDENED RMILTER
# Constraint: debian-slim - C binary compiled from source
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-base \
        libmilter-dev \
        libpcre2-dev \
        curl="7.88.1-*" \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN curl -fsSL "https://github.com/vstakhov/rmilter/archive/refs/tags/${VERSION}.tar.gz" -o /tmp/rmilter.tar.gz && \
    tar -xzf /tmp/rmilter.tar.gz -C /build --strip-components=1 && \
    rm /tmp/rmilter.tar.gz && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release . && \
    make -j$(nproc) && \
    strip rmilter/rmilter

FROM cgr.dev/chainguard/wolfi-base:latest

SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apk add --no-cache libpcre2-8-0 ca-certificates
RUN groupadd -r -g 65532 rmilter && useradd -r -u 65532 -g rmilter -d /var/run/rmilter -s /usr/sbin/nologin rmilter
COPY --from=builder /build/rmilter/rmilter /usr/local/bin/rmilter
RUN mkdir -p /var/run/rmilter /var/log/rmilter && chown -R 65532:65532 /var/run/rmilter /var/log/rmilter
USER 65532:65532
WORKDIR /var/run/rmilter
EXPOSE 6379
ENTRYPOINT ["/usr/local/bin/rmilter"]
LABEL org.opencontainers.image.title="rmilter" \
      org.opencontainers.image.description="Rmilter - milter filter for mail servers" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.vendor="vstakhov" \
      org.opencontainers.image.source="https://github.com/vstakhov/rmilter" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM