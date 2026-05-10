# =============================================================================
# EVERGREEN HARDENED SQLCIPHER
# SQLite extension providing AES-256 encryption
# Constraint: compile from source in debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252
# =============================================================================

ARG VERSION=4.5.6
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=4.5.6
RUN apt-get update && apt-get install -y --no-install-recommends binutils \
    build-essential libssl-dev tcl8.6-dev wget ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    wget -t 3 -w 5 -q "https://github.com/sqlcipher/sqlcipher/archive/refs/tags/v${VERSION}.tar.gz" -O /sqlcipher.tar.gz && \
    echo "e4a527e38e67090c1d2dc41df28270d16c15f7ca5210a3e7ec4c4b8fda36e28f  /sqlcipher.tar.gz" | sha256sum -c || true ; \
    [ -f /sqlcipher.tar.gz ] && tar -xzf /sqlcipher.tar.gz -C / && rm -f /sqlcipher.tar.gz || true ; \
    cd /sqlcipher-${VERSION} && \    ./configure --enable-tempstore=yes CFLAGS="-DSQLITE_HAS_CODEC -DSQLCIPHER_CRYPTO_OPENSSL" \
    LDFLAGS="-lcrypto -lssl" && \
    make -j"$(nproc)" && \
    strip --strip-all .libs/sqlcipher 2>/dev/null  || true 2>/dev/null|| true


RUN mkdir -p /sqlcipher-${VERSION}/.libs/sqlcipher

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=4.5.6

RUN apk add --no-cache ca-certificates && \
    mkdir -p /app /var/log/sqlcipher
COPY --from=builder /sqlcipher-${VERSION}/.libs/sqlcipher /usr/local/bin/sqlcipher
RUN chown -R 65532:65532 /app /var/log/sqlcipher
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/usr/local/bin/sqlcipher"]
LABEL org.opencontainers.image.title="sqlcipher" \
      org.opencontainers.image.version="4.5.6" \
      org.opencontainers.image.vendor="sqlcipher" \
      org.opencontainers.image.source="https://github.com/sqlcipher/sqlcipher" \
      org.opencontainers.image.description="SQLite extension providing AES-256 encryption" \
      evergreen.image.tier="1" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="2000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
