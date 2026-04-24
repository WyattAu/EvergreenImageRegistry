# =============================================================================
# SOVEREIGN HARDENED RMILTER
# Constraint: debian-slim - C binary compiled from source
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION=1.0.0
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libmilter-dev \
        libpcre2-dev \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/vstakhov/rmilter/archive/refs/tags/${VERSION}.tar.gz -o /tmp/rmilter.tar.gz && \
    tar -xzf /tmp/rmilter.tar.gz -C /build --strip-components=1 && \
    rm /tmp/rmilter.tar.gz && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release . && \
    make -j$(nproc) && \
    strip rmilter/rmilter || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache libpcre2-8-0 ca-certificates
RUN addgroup -S -g 65532 rmilter && adduser -u 65532 -G rmilter -D -h /var/run/rmilter -s /sbin/nologin rmilter
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