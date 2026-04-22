# =============================================================================
# SOVEREIGN HARDENED BUNDLER
# Generated from template - Version: 2.5.0
# Constraint: debian-slim - Ruby runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.5.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ruby ruby-dev ca-certificates curl build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN gem install bundler -v 2.5.0 --no-document && \
    strip /usr/local/bin/bundle 2>/dev/null || true && \
    strip /usr/local/bin/bundler 2>/dev/null || true
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/ruby /var/cache/ruby && chown -R app:app /app /var/log/ruby /var/cache/ruby 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["bundle", "--version"]
ENTRYPOINT ["bundle"]
LABEL org.opencontainers.image.title="bundler" \
      org.opencontainers.image.version="2.5.0" \
      org.opencontainers.image.vendor="Ruby Bundler" \
      org.opencontainers.image.source="https://github.com/rubygems/rubygems" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
