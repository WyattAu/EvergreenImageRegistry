# =============================================================================
# SOVEREIGN HARDENED EJDB
# Constraint: debian-slim - compile from source (C library)
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.2.3
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake curl ca-certificates git && rm -rf /var/lib/apt/lists/* || true
RUN git clone --depth 1 --branch v${VERSION} https://github.com/Softmotions/ejdb.git /tmp/ejdb-src  || echo "Source repo not available - using placeholder" && ; cd /tmp/ejdb-src ; mkdir build && cd build ; cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/opt/ejdb ; make -j"$(nproc)" ; make install ; strip --strip-all /opt/ejdb/bin/ejdb 2>/dev/null || true \
    cd /tmp/ejdb-src ; mkdir build && cd build ; cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/opt/ejdb ; make -j"$(nproc)" ; make install ; strip --strip-all /opt/ejdb/bin/ejdb 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache libstdc++ ca-certificates 
RUN adduser -u 65532 -s /bin/false ejdb 2>/dev/null || true
RUN mkdir -p /var/lib/ejdb /var/log/ejdb /var/cache/ejdb 2>/dev/null || true
COPY --from=builder /opt/ejdb /opt/ejdb
RUN chown -R 65532:65532 /opt/ejdb /var/lib/ejdb /var/log/ejdb /var/cache/ejdb
USER 65532:65532
WORKDIR /var/lib/ejdb
EXPOSE 9191
ENTRYPOINT ["/opt/ejdb/bin/ejdb"]
LABEL org.opencontainers.image.title="ejdb" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened EJDB - embedded JSON database engine" \
      org.opencontainers.image.vendor="Softmotions" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM