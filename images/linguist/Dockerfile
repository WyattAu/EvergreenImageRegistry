FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby ruby-dev build-essential git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN gem install github-linguist --no-document
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/lib/ruby/gems /usr/lib/ruby/gems 2>/dev/null || true
COPY --from=builder /usr/local/bundle /usr/local/bundle 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin linguist 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=10s --retries=1 \
    CMD ["linguist", "--version"] || exit 0
ENTRYPOINT ["linguist"]
LABEL org.opencontainers.image.title="linguist" \
      org.opencontainers.image.description="GitHub Linguist - language detection" \
      org.opencontainers.image.vendor="GitHub" \
      org.opencontainers.image.source="https://github.com/github/linguist" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
