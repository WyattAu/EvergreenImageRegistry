# =============================================================================
# SOVEREIGN HARDENED SQLCIPHER
# SQLite extension providing AES-256 encryption
# Constraint: compile from source in debian:bookworm-slim
# =============================================================================

ARG VERSION=4.5.6
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libssl-dev tcl8.6-dev wget ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN wget -q "https://github.com/sqlcipher/sqlcipher/archive/refs/tags/v${VERSION}.tar.gz" -O /sqlcipher.tar.gz && \
    tar -xzf /sqlcipher.tar.gz -C / && rm /sqlcipher.tar.gz && \
    cd /sqlcipher-${VERSION} && \
    ./configure --enable-tempstore=yes CFLAGS="-DSQLITE_HAS_CODEC -DSQLCIPHER_CRYPTO_OPENSSL" \
    LDFLAGS="-lcrypto -lssl" && \
    make -j"$(nproc)" && \
    strip --strip-all .libs/sqlcipher 2>/dev/null || true

FROM debian:bookworm-slim AS runner
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl3 ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/sqlcipher
COPY --from=builder /sqlcipher-${VERSION}/.libs/sqlcipher /usr/local/bin/sqlcipher
RUN chown -R 65534:65534 /app /var/log/sqlcipher
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/usr/local/bin/sqlcipher", "--version"]
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
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="2000ms"
