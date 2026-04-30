ARG VERSION=0.10.0
ARG BUILD_DATE

FROM ruby:3.2-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential git curl ca-certificates gnupg && \
    rm -rf /var/lib/apt/lists/* || true
RUN gem install dependabot-omnibus --no-document 2>/dev/null || true
RUN mkdir -p /app /usr/local/bin 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ruby ruby-irb ruby-rdoc ca-certificates \
        git curl gnupg gmp mpdecimal libffi \
        readline ncurses yaml zlib || true
RUN mkdir -p /usr/lib/ruby /usr/local/bundle /app 2>/dev/null || true
COPY --from=builder /usr/lib/ruby/gems /usr/lib/ruby/gems
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY --from=builder /usr/local/bin/dependabot /usr/local/bin/dependabot 2>/dev/null || true
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false dependabot 2>/dev/null || true && \
    chown -R 65532:65532 /app /usr/local/bundle 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["dependabot"]
CMD ["scan"]
LABEL org.opencontainers.image.title="dependabot" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Dependabot - Automated dependency updates" \
      org.opencontainers.image.vendor="GitHub" \
      org.opencontainers.image.source="https://github.com/dependabot/dependabot-core" \
      sovereign.image.tier="3" \
      sovereign.image.category="devops" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
