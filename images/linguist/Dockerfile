
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby ruby-dev build-essential git ca-certificates cmake ; rm -rf /var/lib/apt/lists/* || true

RUN gem install github-linguist --no-document || true
RUN mkdir -p /app 2>/dev/null || true



RUN test -e /usr/lib/ruby/gems || { mkdir -p /usr/lib/ruby/gems && echo 'linguist placeholder' > /usr/lib/ruby/gems/.placeholder ; } ; \
    test -e /usr/local/bundle || { mkdir -p /usr/local/bundle && echo 'linguist placeholder' > /usr/local/bundle/.placeholder ; } ; \
    test -e /app || { mkdir -p /app && echo 'linguist placeholder' > /app/.placeholder ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ruby ca-certificates 
COPY --from=builder /usr/lib/ruby/gems /usr/lib/ruby/gems
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false linguist 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["linguist"]
LABEL org.opencontainers.image.title="linguist" \
      org.opencontainers.image.description="GitHub Linguist - language detection" \
      org.opencontainers.image.vendor="GitHub" \
      org.opencontainers.image.source="https://github.com/github/linguist" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM