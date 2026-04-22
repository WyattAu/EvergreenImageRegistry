# =============================================================================
# SOVEREIGN HARDENED KNOT-RESOLVER
# Full-featured DNS recursive resolver (C/luajit)
# Constraint: compile from source in debian:bookworm-slim
# =============================================================================

ARG VERSION=5.7.6
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-base cmake libssl-dev libluajit-5.1-dev libsystemd-dev \
    libuv1-dev libnghttp2-dev meson pkgconf git ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch "v${VERSION}" \
    https://github.com/CZ-NIC/knot-resolver.git /knot-resolver
RUN cd /knot-resolver && \
    meson setup build --default-library=static --prefix=/usr \
    -Dclient=enabled -Dpostinst=disabled && \
    meson compile -C build -j"$(nproc)" && \
    strip --strip-all /knot-resolver/build/kresd 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache libnghttp2-14 ca-certificates
RUN mkdir -p /app /var/log/knot-resolver /var/lib/knot-resolver /etc/knot-resolver
COPY --from=builder /knot-resolver/build/kresd /usr/local/bin/kresd
COPY --from=builder /knot-resolver/build/rootkeys.list /etc/knot-resolver/rootkeys.list 2>/dev/null || true
RUN chown -R 65532:65532 /app /var/log/knot-resolver /var/lib/knot-resolver
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 8453
ENTRYPOINT ["/usr/local/bin/kresd"]
LABEL org.opencontainers.image.title="knot-resolver" \
      org.opencontainers.image.version="5.7.6" \
      org.opencontainers.image.vendor="CZ.NIC" \
      org.opencontainers.image.source="https://github.com/CZ-NIC/knot-resolver" \
      org.opencontainers.image.description="Full-featured DNS recursive resolver" \
      sovereign.image.tier="1" \
      sovereign.image.category="dns" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM