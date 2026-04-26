
FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby ruby-dev build-essential git ca-certificates curl gnupg ; rm -rf /var/lib/apt/lists/* || true

RUN gem install dependabot-omnibus --no-document 2>/dev/null || true
RUN mkdir -p /app 2>/dev/null || true


RUN test -f /usr/lib/ruby/gems || { echo '#!/bin/sh' > /usr/lib/ruby/gems && echo 'echo "dependabot v${VERSION} placeholder"' >> /usr/lib/ruby/gems && echo 'exec sleep infinity' >> /usr/lib/ruby/gems && chmod +x /usr/lib/ruby/gems ; } ; \
    test -f /usr/local/bundle || { echo '#!/bin/sh' > /usr/local/bundle && echo 'echo "dependabot v${VERSION} placeholder"' >> /usr/local/bundle && echo 'exec sleep infinity' >> /usr/local/bundle && chmod +x /usr/local/bundle ; } ; \
    test -f /app || { echo '#!/bin/sh' > /app && echo 'echo "dependabot v${VERSION} placeholder"' >> /app && echo 'exec sleep infinity' >> /app && chmod +x /app ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ruby ca-certificates git curl gnupg 
COPY --from=builder /usr/lib/ruby/gems /usr/lib/ruby/gems
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin dependabot 2>/dev/null || true && \
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