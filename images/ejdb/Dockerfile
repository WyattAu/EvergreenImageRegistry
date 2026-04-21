# =============================================================================
# SOVEREIGN HARDENED EJDB
# Constraint: debian-slim - compile from source (C library)
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.2.3
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake curl ca-certificates git && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN git clone --depth 1 --branch v${VERSION} https://github.com/Softmotions/ejdb.git /tmp/ejdb-src \
    && cd /tmp/ejdb-src \
    && mkdir build && cd build \
    && cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/opt/ejdb \
    && make -j"$(nproc)" \
    && make install \
    && strip --strip-all /opt/ejdb/bin/ejdb 2>/dev/null || true

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    libstdc++6 ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin ejdb 2>/dev/null || true
RUN mkdir -p /var/lib/ejdb /var/log/ejdb /var/cache/ejdb
COPY --from=builder /opt/ejdb /opt/ejdb
RUN chown -R 65534:65534 /opt/ejdb /var/lib/ejdb /var/log/ejdb /var/cache/ejdb
USER 65534:65534
WORKDIR /var/lib/ejdb
EXPOSE 9191
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/opt/ejdb/bin/ejdb", "--version"]
ENTRYPOINT ["/opt/ejdb/bin/ejdb"]
LABEL org.opencontainers.image.title="ejdb" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened EJDB - embedded JSON database engine" \
      org.opencontainers.image.vendor="Softmotions" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
