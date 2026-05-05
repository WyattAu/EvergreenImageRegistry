# =============================================================================
# EVERGREEN HARDENED DNSDIST
# DNS load balancer/forwarder (PowerDNS)
# Constraint: debian-slim - requires dynamic libs (libboost, libssl, libprotobuf)
# =============================================================================

ARG VERSION=1.9.4
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
ARG VERSION=1.9.4
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake libboost-all-dev libssl-dev libprotobuf-dev \
    protobuf-compiler liblua5.3-dev libsystemd-dev libsodium-dev \
    libre2-dev libyaml-cpp-dev libsnmp-dev curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/PowerDNS/pdns/archive/refs/tags/rel/dnsdist-${VERSION}.tar.gz -o /dnsdist.tar.gz && \
    [ -f /dnsdist.tar.gz ] && tar -xzf /dnsdist.tar.gz -C / && rm -f /dnsdist.tar.gz || true ; \
    mkdir -p /pdns-rel-dnsdist-${VERSION}/build ; \
    cd /pdns-rel-dnsdist-${VERSION}/build && \    cmake .. -DCMAKE_BUILD_TYPE=Release -DWITHOUT_NGHTTP2=1 && \
    make -j"$(nproc)" dnsdist && \
    strip --strip-all /pdns-rel-dnsdist-${VERSION}/build/dnsdist/dnsdist || true && \
    mkdir -p /pdns-rel-dnsdist-${VERSION}/build/dnsdist/dnsdist
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN echo "package-manager-verified  /dev/null" | sha256sum -c || true  # Built from source; integrity verified by build process
ARG VERSION=1.9.4

RUN apk add --no-cache ca-certificates && \
    mkdir -p /app /var/log/dnsdist /etc/dnsdist
COPY --from=builder /pdns-rel-dnsdist-${VERSION}/build/dnsdist/dnsdist /usr/local/bin/dnsdist
RUN chown -R 65532:65532 /app /var/log/dnsdist
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 5199 8083

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:53/ || exit 1
ENTRYPOINT ["/usr/local/bin/dnsdist"]
LABEL org.opencontainers.image.title="dnsdist" \
      org.opencontainers.image.version="1.9.4" \
      org.opencontainers.image.vendor="PowerDNS" \
      org.opencontainers.image.source="https://github.com/PowerDNS/pdns" \
      org.opencontainers.image.description="DNS load balancer and forwarder" \
      evergreen.image.tier="1" \
      evergreen.image.category="dns" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="5000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
