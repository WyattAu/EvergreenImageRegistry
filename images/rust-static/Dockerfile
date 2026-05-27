ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=1.78.0
ARG TARGETARCH
RUN mkdir -p /opt/rust || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    ARCH="${TARGETARCH:-amd64}" && \
    case "$ARCH" in \
        amd64) RUST_ARCH="x86_64-unknown-linux-gnu" ;; \
        arm64) RUST_ARCH="aarch64-unknown-linux-gnu" ;; \
        *) echo "Unsupported architecture: $ARCH" && exit 1 ;; \
    esac && \
    curl --retry 3 --retry-delay 5 -fsSL \
    "https://static.rust-lang.org/dist/rust-${VERSION}-${RUST_ARCH}.tar.xz" \
    -o /rust.tar.xz && \
    mkdir -p /tmp/rust && \
    tar -xf /rust.tar.xz -C /tmp/rust --strip-components=1 && \
    rm -f /rust.tar.xz && \
    /tmp/rust/install.sh --prefix=/opt/rust \
        --components=rust-std,cargo,rustc,rust-std-${RUST_ARCH/-gnu/-musl} \
        --without=rust-docs --without=rustfmt --without=clippy && \
    strip /opt/rust/bin/rustc /opt/rust/bin/cargo 2>/dev/null
FROM scratch
COPY --from=builder /opt/rust /opt/rust
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
ENV PATH="/opt/rust/bin:${PATH}" \
    CARGO_HOME=/app/.cargo \
    RUSTUP_HOME=/app/.rustup
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/opt/rust/bin/rustc"]
CMD ["--version"]
LABEL org.opencontainers.image.title="rust-static" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Rust" \
      org.opencontainers.image.description="Evergreen hardened rust-static - Rust static compilation base" \
      org.opencontainers.image.source="https://www.rust-lang.org/" \
      evergreen.image.tier="3" \
      evergreen.image.category="build-tool" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
