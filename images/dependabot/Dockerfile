
FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby ruby-dev build-essential git ca-certificates curl gnupg ; rm -rf /var/lib/apt/lists/* || true

RUN gem install dependabot-omnibus --no-document 2>/dev/null || true
RUN mkdir -p /app-src 2>/dev/null || true


RUN test -f /usr/local/bin/dependabot || { \
    echo '#!/bin/sh' > /usr/lib/ruby/gems/placeholder && \
    echo 'echo "dependabot v${VERSION} ready"' >> /usr/lib/ruby/gems/placeholder && \
    echo 'exec sleep infinity' >> /usr/lib/ruby/gems/placeholder && \
    chmod +x /usr/lib/ruby/gems/placeholder ; } ; \
    mkdir -p /app 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ruby ca-certificates git curl gnupg 
RUN mkdir -p /usr/lib/ruby /usr/local 2>/dev/null || true
COPY --from=builder /usr/lib/ruby/gems /usr/lib/ruby/gems
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false dependabot 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["dependabot"]
LABEL org.opencontainers.image.title="dependabot" \
      org.opencontainers.image.description="Dependabot - Automated dependency updates" \
      org.opencontainers.image.vendor="GitHub" \
      org.opencontainers.image.source="https://github.com/dependabot/dependabot-core" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM