FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby ruby-dev build-base ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN gem install bundler-audit --no-document
RUN mkdir -p /app

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ruby ca-certificates
COPY --from=builder /usr/lib/ruby/gems /usr/lib/ruby/gems 2>/dev/null || true
COPY --from=builder /usr/local/bundle /usr/local/bundle 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin gemaudit 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["bundler-audit"]
LABEL org.opencontainers.image.title="gem-audit" \
      org.opencontainers.image.description="Gem/Bundler audit - Ruby dependency security scanner" \
      org.opencontainers.image.vendor="rubysec" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM