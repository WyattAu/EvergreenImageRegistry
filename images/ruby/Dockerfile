# =============================================================================
# SOVEREIGN HARDENED RUBY
# Generated from template - Version: 3.3.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.3.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ruby ruby-bundler ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' ruby 2>/dev/null || true
RUN mkdir -p /app /var/log/ruby /var/cache/ruby && chown -R ruby:ruby /app /var/log/ruby /var/cache/ruby 2>/dev/null || true
USER ruby
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ruby ruby --version
ENTRYPOINT ["ruby"]
LABEL org.opencontainers.image.title="ruby" \
      org.opencontainers.image.version="3.3.1" \
      org.opencontainers.image.vendor="Ruby" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
