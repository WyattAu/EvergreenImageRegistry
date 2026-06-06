ARG VERSION=0.10.1
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends binutils \
        build-essential cmake g++ \
        libqt5widgets5 libqt5core5a qtbase5-dev \
        ca-certificates curl git && \
    rm -rf /var/lib/apt/lists/* || true && \
    git clone --branch "v${VERSION}" https://github.com/Eqonomize/Eqonomize.git /tmp/eqonomize ; \
    cd /tmp/eqonomize && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE=Release . && \
    make -j$(nproc) && make install && strip --strip-all /usr/local/bin/eqonomize 2>/dev/null
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates

COPY --from=builder /usr/local/bin/eqonomize /usr/local/bin/eqonomize
RUN mkdir -p /app /var/log/eqonomize /var/cache/eqonomize ; \
    chown -R 65532:65532 /app /var/log/eqonomize /var/cache/eqonomize
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["eqonomize"]
LABEL org.opencontainers.image.title="eqonomize" \
      org.opencontainers.image.description="eqonomize container image" \
      org.opencontainers.image.version="0.10.1" \
      org.opencontainers.image.vendor="Eqonomize" \
      org.opencontainers.image.source="https://github.com/Eqonomize/Eqonomize" \
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
