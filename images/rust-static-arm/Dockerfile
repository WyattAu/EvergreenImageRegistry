FROM debian:bookworm-slim AS builder
ARG VERSION=1.78.0
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL \
    "https://static.rust-lang.org/dist/rust-${VERSION}-aarch64-unknown-linux-gnu.tar.xz" \
    -o /rust.tar.xz && \
    echo "e33789c7c32d89cbb939b2f58b7651c736cb9f37e42e11152cda7cc33df686a0  /rust.tar.xz" | sha256sum -c - && \
    mkdir -p /tmp/rust && \
    tar -xf /rust.tar.xz -C /tmp/rust --strip-components=1 && \
    rm /rust.tar.xz && \
    /tmp/rust/install.sh --prefix=/opt/rust \
        --components=rust-std,cargo,rustc,rust-std-aarch64-unknown-linux-musl \
        --without=rust-docs --without=rustfmt --without=clippy && \
    strip /opt/rust/bin/rustc /opt/rust/bin/cargo 2>/dev/null || true

FROM scratch
COPY --from=builder /opt/rust /opt/rust
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
ENV PATH="/opt/rust/bin:${PATH}" \
    CARGO_HOME=/app/.cargo \
    RUSTUP_HOME=/app/.rustup
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/opt/rust/bin/rustc"]
CMD ["--version"]
LABEL org.opencontainers.image.title="rust-static-arm" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Rust" \
      org.opencontainers.image.description="Sovereign hardened rust-static-arm - Rust static base for ARM64" \
      org.opencontainers.image.source="https://www.rust-lang.org/" \
      sovereign.image.tier="3" \
      sovereign.image.category="build-tool" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
