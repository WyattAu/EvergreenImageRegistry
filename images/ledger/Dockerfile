ARG VERSION=3.3.2
ARG BUILD_DATE
ARG TARGETARCH


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential cmake g++ libboost-all-dev libgmp-dev \
        libmpfr-dev texinfo groff curl git ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    git clone --depth 1 --branch "v${VERSION}" https://github.com/ledger/ledger.git /tmp/ledger 2>/dev/null || true && \
    cd /tmp/ledger && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr/local -DBUILD_DOCS=OFF -DUSE_PYTHON=OFF . && \
    make -j$(nproc) && make install && strip --strip-all /usr/local/bin/ledger 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache git ca-certificates || true
COPY --from=builder /usr/local/bin/ledger /usr/local/bin/ledger
RUN mkdir -p /app /var/log/ledger /var/cache/ledger ; \
    chown -R 65532:65532 /app /var/log/ledger /var/cache/ledger || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["ledger"]
LABEL org.opencontainers.image.title="ledger" \
      org.opencontainers.image.version="3.3.2" \
      org.opencontainers.image.vendor="Ledger" \
      org.opencontainers.image.source="https://github.com/ledger/ledger" \
      evergreen.image.tier="2" \
      evergreen.image.category="business-finance" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="10000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
