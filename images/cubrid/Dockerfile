# =============================================================================
# SOVEREIGN HARDENED CUBRID
# Constraint: debian-slim - compile from source
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=11.2
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake curl ca-certificates libncurses5-dev \
    libedit-dev && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/CUBRID/cubrid/releases/download/CUBRID_${VERSION}/cubrid-${VERSION}-src.tar.gz" -o /tmp/cubrid.tar.gz \
    && echo "PENDING  /tmp/cubrid.tar.gz" | sha256sum -c - \
    && tar -xzf /tmp/cubrid.tar.gz -C /tmp \
    && cd /tmp/cubrid-${VERSION} \
    && mkdir build && cd build \
    && cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/opt/cubrid \
    && make -j"$(nproc)" \
    && make install \
    && strip --strip-all /opt/cubrid/bin/cubrid /opt/cubrid/bin/cub_server 2>/dev/null || true

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    libncurses5 libedit2 ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin cubrid 2>/dev/null || true
RUN mkdir -p /var/lib/cubrid /var/log/cubrid /var/cache/cubrid
COPY --from=builder /opt/cubrid /opt/cubrid
RUN chown -R 65534:65534 /opt/cubrid /var/lib/cubrid /var/log/cubrid /var/cache/cubrid
USER 65534:65534
WORKDIR /var/lib/cubrid
EXPOSE 30000 33000 33001
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["/opt/cubrid/bin/cubrid", "service", "status"]
ENTRYPOINT ["/opt/cubrid/bin/cubrid"]
LABEL org.opencontainers.image.title="cubrid" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened CUBRID - open source SQL database" \
      org.opencontainers.image.vendor="CUBRID" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
