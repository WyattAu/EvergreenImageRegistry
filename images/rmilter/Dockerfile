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
        build-essential \
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

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libmilter1.0.1 \
        libpcre2-8-0 \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN groupadd -r -g 65534 rmilter && useradd -r -u 65534 -g rmilter -d /var/run/rmilter -s /usr/sbin/nologin rmilter
COPY --from=builder /build/rmilter/rmilter /usr/local/bin/rmilter
RUN mkdir -p /var/run/rmilter /var/log/rmilter && chown -R 65534:65534 /var/run/rmilter /var/log/rmilter
USER 65534:65534
WORKDIR /var/run/rmilter
EXPOSE 6379
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/rmilter", "-h"]
ENTRYPOINT ["/usr/local/bin/rmilter"]
LABEL org.opencontainers.image.title="rmilter" \
      org.opencontainers.image.description="Rmilter - milter filter for mail servers" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.vendor="vstakhov" \
      org.opencontainers.image.source="https://github.com/vstakhov/rmilter" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true"
