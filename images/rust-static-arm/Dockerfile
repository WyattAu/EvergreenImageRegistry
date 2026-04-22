ARG VERSION=stable
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://static.rust-lang.org/dist/rust-1.80.1-aarch64-unknown-linux-gnu.tar.xz" -o /rust.tar.xz && \
    mkdir -p /tmp/rust && tar -xf /rust.tar.xz -C /tmp/rust --strip-components=1 && rm /rust.tar.xz && \
    /tmp/rust/install.sh --prefix=/opt/rust --components=rust-std,cargo,rustc --without=rust-docs --without=rustfmt --without=clippy && \
    strip /opt/rust/bin/rustc /opt/rust/bin/cargo 2>/dev/null || true

FROM scratch
COPY --from=downloader /opt/rust /opt/rust
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
ENV PATH="/opt/rust/bin:${PATH}" \
    CARGO_HOME=/app/.cargo \
    RUSTUP_HOME=/app/.rustup
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="rust-static-arm" \
      org.opencontainers.image.version="1.80.1" \
      org.opencontainers.image.vendor="Rust" \
      org.opencontainers.image.description="Sovereign hardened rust-static-arm - Rust static base for ARM64" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM