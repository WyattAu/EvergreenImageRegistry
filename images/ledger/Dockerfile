ARG VERSION=3.3.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential cmake g++ libboost-all-dev libgmp-dev \
        libmpfr-dev texinfo groff curl ca-certificates git && \
    rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch v{version} \
    "https://github.com/ledger/ledger.git" /tmp/ledger && \
    cd /tmp/ledger && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr/local -DBUILD_DOCS=OFF -DUSE_PYTHON=OFF . && \
    make -j$(nproc) && make install && strip /usr/local/bin/ledger

FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        libboost-iostreams1.74.0 libgmp10 libmpfr6 ca-certificates && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/bin/ledger /usr/local/bin/ledger
RUN mkdir -p /app /var/log/ledger /var/cache/ledger && \
    chown -R 65534:65534 /app /var/log/ledger /var/cache/ledger
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["ledger", "--version"]
ENTRYPOINT ["ledger"]
LABEL org.opencontainers.image.title="ledger" \
      org.opencontainers.image.version="3.3.2" \
      org.opencontainers.image.vendor="Ledger" \
      org.opencontainers.image.source="https://github.com/ledger/ledger" \
      sovereign.image.tier="2" \
      sovereign.image.category="business-finance" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
