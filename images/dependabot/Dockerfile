FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby ruby-dev build-base git ca-certificates curl gnupg \
    && rm -rf /var/lib/apt/lists/*
RUN gem install dependabot-omnibus --no-document 2>/dev/null || true
RUN mkdir -p /app

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ruby ca-certificates git curl gnupg
COPY --from=builder /usr/lib/ruby/gems /usr/lib/ruby/gems 2>/dev/null || true
COPY --from=builder /usr/local/bundle /usr/local/bundle 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin dependabot 2>/dev/null || true && \
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
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM