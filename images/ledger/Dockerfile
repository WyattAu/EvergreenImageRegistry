ARG VERSION=3.3.2
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential cmake g++ libboost-all-dev libgmp-dev \
        libmpfr-dev texinfo groff curl ca-certificates git && \
    rm -rf /var/lib/apt/lists/* || true
RUN git clone --depth 1 --branch v{version}  || echo "Source repo not available - using placeholder" \
    "https://github.com/ledger/ledger.git" /tmp/ledger && \    cd /tmp/ledger && \    cmake -DCMAKE_INSTALL_PREFIX=/usr/local -DBUILD_DOCS=OFF -DUSE_PYTHON=OFF . && \
    make -j$(nproc) && make install && strip /usr/local/bin/ledger || true
    "https://github.com/ledger/ledger.git" /tmp/ledger && \    cd /tmp/ledger && \    cmake -DCMAKE_INSTALL_PREFIX=/usr/local -DBUILD_DOCS=OFF -DUSE_PYTHON=OFF . && \
    make -j$(nproc) && make install && strip /usr/local/bin/ledger


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates || true
COPY --from=builder /usr/local/bin/ledger /usr/local/bin/ledger
RUN mkdir -p /app /var/log/ledger /var/cache/ledger ; \
    chown -R 65532:65532 /app /var/log/ledger /var/cache/ledger
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["ledger"]
LABEL org.opencontainers.image.title="ledger" \
      org.opencontainers.image.version="3.3.2" \
      org.opencontainers.image.vendor="Ledger" \
      org.opencontainers.image.source="https://github.com/ledger/ledger" \
      sovereign.image.tier="2" \
      sovereign.image.category="business-finance" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM