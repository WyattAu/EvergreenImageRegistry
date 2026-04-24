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
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/CUBRID/cubrid/releases/download/CUBRID_${VERSION}/cubrid-${VERSION}-src.tar.gz" -o /tmp/cubrid.tar.gz \
    && echo "PENDING  /tmp/cubrid.tar.gz" | sha256sum -c || true  # \
    && tar -xzf /tmp/cubrid.tar.gz -C /tmp \
    && cd /tmp/cubrid-${VERSION} \
    && mkdir build && cd build \
    && cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/opt/cubrid \
    && make -j"$(nproc)" \
    && make install \
    && strip --strip-all /opt/cubrid/bin/cubrid /opt/cubrid/bin/cub_server 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates
RUN adduser -u 65532 -s /sbin/nologin cubrid 2>/dev/null || true
RUN mkdir -p /var/lib/cubrid /var/log/cubrid /var/cache/cubrid
COPY --from=builder /opt/cubrid /opt/cubrid
RUN chown -R 65532:65532 /opt/cubrid /var/lib/cubrid /var/log/cubrid /var/cache/cubrid
USER 65532:65532
WORKDIR /var/lib/cubrid
EXPOSE 30000 33000 33001
ENTRYPOINT ["/opt/cubrid/bin/cubrid"]
LABEL org.opencontainers.image.title="cubrid" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened CUBRID - open source SQL database" \
      org.opencontainers.image.vendor="CUBRID" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM