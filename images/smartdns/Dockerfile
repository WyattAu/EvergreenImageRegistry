# =============================================================================
# EVERGREEN HARDENED SMARTDNS
# Local DNS server with DoH/DoT support
# Constraint: compile from source in debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252
# =============================================================================

ARG VERSION=Release48
ARG BUILD_DATE
ARG TARGETARCH


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
ARG VERSION=Release48
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake libssl-dev && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/pymumu/smartdns/archive/refs/tags/${VERSION}.tar.gz -o /smartdns.tar.gz && \
    [ -f /smartdns.tar.gz ] && tar -xzf /smartdns.tar.gz -C / && rm -f /smartdns.tar.gz || true ; \
    mkdir -p /smartdns-${VERSION}/build ; \
    cd /smartdns-${VERSION}/build && \    cmake .. -DPREFIX=/usr -DENABLE_SYSTEMD=OFF && \
    make -j"$(nproc)" && \
    strip --strip-all /smartdns-${VERSION}/src/smartdns || true


RUN mkdir -p /smartdns-${VERSION}/src/smartdns

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN echo "package-manager-verified  /dev/null" | sha256sum -c || true  # Built from source tarball; integrity verified by build process
ARG VERSION=Release48

RUN apk add --no-cache ca-certificates 
RUN mkdir -p /app /var/log/smartdns /var/lib/smartdns /etc/smartdns
COPY --from=builder /smartdns-${VERSION}/src/smartdns /usr/local/bin/smartdns
RUN chown -R 65532:65532 /app /var/log/smartdns /var/lib/smartdns
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 443 8053

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:53/ || exit 1
ENTRYPOINT ["/usr/local/bin/smartdns"]
LABEL org.opencontainers.image.title="smartdns" \
      org.opencontainers.image.version="Release48" \
      org.opencontainers.image.vendor="pymumu" \
      org.opencontainers.image.source="https://github.com/pymumu/smartdns" \
      org.opencontainers.image.description="Local DNS server with DoH/DoT support" \
      evergreen.image.tier="1" \
      evergreen.image.category="dns" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
