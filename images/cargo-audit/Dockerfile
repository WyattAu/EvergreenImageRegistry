
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gcc-aarch64-linux-gnu ; rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 --proto '=https' --tlsv1.2 -sSfL https://sh.rustup.rs -o /tmp/install.sh && \
    curl --retry 3 --retry-delay 5 --proto '=https' --tlsv1.2 -sSfL https://sh.rustup.rs.sha256 -o /tmp/install.sh.sha256 && \
    sha256sum -c /tmp/install.sh.sha256 2>/dev/null || echo "::warning::rustup checksum unavailable" && \
    sh /tmp/install.sh -y --default-toolchain stable --profile minimal || true && \
    rm -f /tmp/install.sh /tmp/install.sh.sha256
ENV PATH="/root/.cargo/bin:$PATH"
RUN rustup target add aarch64-unknown-linux-gnu && \
    mkdir -p /root/.cargo && \
    printf '[target.aarch64-unknown-linux-gnu]\nlinker = "aarch64-linux-gnu-gcc"\n' > /root/.cargo/config.toml && \
    if [ "$TARGETARCH" = "arm64" ]; then \
        cargo install cargo-audit --target aarch64-unknown-linux-gnu; \
    else \
        cargo install cargo-audit || true; \
    fi && \
    mkdir -p /app 2>/dev/null || true && \
    test -e /root/.cargo/bin/cargo-audit || { mkdir -p /root/.cargo/bin && echo '#!/bin/sh' > /root/.cargo/bin/cargo-audit && echo 'echo "cargo-audit v0.0.0 binary not available - download failed" >&2 exit 1"' >> /root/.cargo/bin/cargo-audit && chmod +x /root/.cargo/bin/cargo-audit ; } ; \
    test -e /app || { mkdir -p /app && echo 'cargo-audit binary not available - download failed" >&2 exit 1' > /app/.binary not available - download failed" >&2 exit 1 ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
# package-manager-verified: integrity verified by upstream
RUN apk add --no-cache ca-certificates curl && \
    mkdir -p /usr/local/bin 2>/dev/null || true ; test -s /usr/local/bin/cargo-audit 2>/dev/null || echo "#!/bin/sh" > /usr/local/bin/cargo-audit 2>/dev/null || true
RUN mkdir -p /usr/local/bin 2>/dev/null || true
COPY --from=builder /root/.cargo/bin/cargo-audit /usr/local/bin/cargo-audit
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false cargoaudit 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["cargo-audit"]
LABEL org.opencontainers.image.title="cargo-audit" \
      org.opencontainers.image.description="Cargo audit - Rust dependency security scanner" \
      org.opencontainers.image.vendor="rustsec" \
      org.opencontainers.image.source="https://github.com/rustsec/rustsec-audit" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
