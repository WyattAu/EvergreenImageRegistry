# =============================================================================
# SOVEREIGN HARDENED SQLCIPHER
# SQLite extension providing AES-256 encryption
# Constraint: compile from source in debian:bookworm-slim
# =============================================================================

ARG VERSION=4.5.6
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG VERSION=4.5.6
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-base libssl-dev tcl8.6-dev wget ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN wget -q "https://github.com/sqlcipher/sqlcipher/archive/refs/tags/v${VERSION}.tar.gz" -O /sqlcipher.tar.gz && \
    tar -xzf /sqlcipher.tar.gz -C / && rm /sqlcipher.tar.gz && \
    cd /sqlcipher-${VERSION} && \    ./configure --enable-tempstore=yes CFLAGS="-DSQLITE_HAS_CODEC -DSQLCIPHER_CRYPTO_OPENSSL" \
    LDFLAGS="-lcrypto -lssl" && \
    make -j"$(nproc)" && \
    strip --strip-all .libs/sqlcipher 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=4.5.6

RUN apk add --no-cache ca-certificates
RUN mkdir -p /app /var/log/sqlcipher
COPY --from=builder /sqlcipher-${VERSION}/.libs/sqlcipher /usr/local/bin/sqlcipher
RUN chown -R 65532:65532 /app /var/log/sqlcipher
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/sqlcipher"]
LABEL org.opencontainers.image.title="sqlcipher" \
      org.opencontainers.image.version="4.5.6" \
      org.opencontainers.image.vendor="sqlcipher" \
      org.opencontainers.image.source="https://github.com/sqlcipher/sqlcipher" \
      org.opencontainers.image.description="SQLite extension providing AES-256 encryption" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="2000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM