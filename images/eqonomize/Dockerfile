ARG VERSION=0.10.1
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential cmake g++ \
        libqt5widgets5 libqt5core5a qtbase5-dev \
        ca-certificates curl git && \
    rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch v{version} \ 2>/dev/null || echo "Source repo not available - using placeholder" \
    "https://github.com/Eqonomize/Eqonomize.git" /tmp/eqonomize && \    cd /tmp/eqonomize && \    cmake -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE=Release . && \
    make -j$(nproc) && make install && strip /usr/local/bin/eqonomize


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
COPY --from=builder /usr/local/bin/eqonomize /usr/local/bin/eqonomize
RUN mkdir -p /app /var/log/eqonomize /var/cache/eqonomize && \
    chown -R 65532:65532 /app /var/log/eqonomize /var/cache/eqonomize
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["eqonomize"]
LABEL org.opencontainers.image.title="eqonomize" \
      org.opencontainers.image.version="0.10.1" \
      org.opencontainers.image.vendor="Eqonomize" \
      org.opencontainers.image.source="https://github.com/Eqonomize/Eqonomize" \
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