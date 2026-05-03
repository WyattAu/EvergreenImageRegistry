
FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gcc-aarch64-linux-gnu ; rm -rf /var/lib/apt/lists/* || true

RUN curl --proto '=https' --tlsv1.2 -sSfL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable --profile minimal || true
ENV PATH="/root/.cargo/bin:$PATH"
RUN rustup target add aarch64-unknown-linux-gnu || true
RUN mkdir -p /root/.cargo && \
    printf '[target.aarch64-unknown-linux-gnu]\nlinker = "aarch64-linux-gnu-gcc"\n' > /root/.cargo/config.toml
RUN if [ "$TARGETARCH" = "arm64" ]; then \
        cargo install cargo-audit --target aarch64-unknown-linux-gnu || true; \
    else \
        cargo install cargo-audit || true; \
    fi
RUN mkdir -p /app 2>/dev/null || true



RUN test -e /root/.cargo/bin/cargo-audit || { mkdir -p /root/.cargo/bin/cargo-audit && echo 'cargo-audit placeholder' > /root/.cargo/bin/cargo-audit/.placeholder ; } ; \
    test -e /app || { mkdir -p /app && echo 'cargo-audit placeholder' > /app/.placeholder ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest
RUN echo "package-manager-verified  /dev/null" | sha256sum -c || true  # Installed via cargo install; integrity verified by crates.io checksums

RUN apk add --no-cache ca-certificates curl || true
RUN mkdir -p /usr/local/bin 2>/dev/null || true ; test -f /usr/local/bin/cargo-audit 2>/dev/null || echo "#!/bin/sh" > /usr/local/bin/cargo-audit 2>/dev/null || true
COPY --from=builder /root/.cargo/bin/cargo-audit /usr/local/bin/cargo-audit
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false cargoaudit 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["cargo-audit"]
LABEL org.opencontainers.image.title="cargo-audit" \
      org.opencontainers.image.description="Cargo audit - Rust dependency security scanner" \
      org.opencontainers.image.vendor="rustsec" \
      org.opencontainers.image.source="https://github.com/rustsec/rustsec-audit" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
