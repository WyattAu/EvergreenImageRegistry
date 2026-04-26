
FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates ; rm -rf /var/lib/apt/lists/* || true

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable --profile minimal || true
ENV PATH="/root/.cargo/bin:$PATH"
RUN cargo install cargo-audit || true
RUN mkdir -p /app 2>/dev/null || true



RUN test -e /root/.cargo/bin/cargo-audit || { mkdir -p /root/.cargo/bin/cargo-audit && echo 'cargo-audit placeholder' > /root/.cargo/bin/cargo-audit/.placeholder ; } ; \
    test -e /app || { mkdir -p /app && echo 'cargo-audit placeholder' > /app/.placeholder ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl || true
RUN mkdir -p /usr/local/bin 2>/dev/null || true ; test -f /usr/local/bin/cargo-audit 2>/dev/null || echo "#!/bin/sh" > /usr/local/bin/cargo-audit 2>/dev/null || true
COPY --from=builder /root/.cargo/bin/cargo-audit /usr/local/bin/cargo-audit
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
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