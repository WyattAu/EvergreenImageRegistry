# =============================================================================
# SOVEREIGN HARDENED BUNDLER
# Generated from template - Version: 2.5.0
# Constraint: debian-slim - Ruby runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.5.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ruby ruby-dev ca-certificates curl build-base
RUN gem install bundler -v 2.5.0 --no-document && \
    strip /usr/local/bin/bundle 2>/dev/null || true && \
    strip /usr/local/bin/bundler 2>/dev/null || true
RUN useradd -m -u 65532 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/ruby /var/cache/ruby && chown -R app:app /app /var/log/ruby /var/cache/ruby 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["bundle"]
LABEL org.opencontainers.image.title="bundler" \
      org.opencontainers.image.version="2.5.0" \
      org.opencontainers.image.vendor="Ruby Bundler" \
      org.opencontainers.image.source="https://github.com/rubygems/rubygems" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM