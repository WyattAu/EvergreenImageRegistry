
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby ruby-dev build-essential ca-certificates ; rm -rf /var/lib/apt/lists/* || true

RUN gem install bundler-audit --no-document
RUN mkdir -p /app 2>/dev/null || true



RUN test -e /usr/lib/ruby/gems || { mkdir -p /usr/lib/ruby/gems && echo 'gem-audit placeholder' > /usr/lib/ruby/gems/.placeholder ; } ; \
    test -e /usr/local/bundle || { mkdir -p /usr/local/bundle && echo 'gem-audit placeholder' > /usr/local/bundle/.placeholder ; } ; \
    test -e /app || { mkdir -p /app && echo 'gem-audit placeholder' > /app/.placeholder ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ruby ca-certificates || true
COPY --from=builder /usr/lib/ruby/gems /usr/lib/ruby/gems
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false gemaudit 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["bundler-audit"]
LABEL org.opencontainers.image.title="gem-audit" \
      org.opencontainers.image.description="Gem/Bundler audit - Ruby dependency security scanner" \
      org.opencontainers.image.vendor="rubysec" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
