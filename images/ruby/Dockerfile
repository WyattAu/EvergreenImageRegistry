# =============================================================================
# SOVEREIGN HARDENED RUBY
# Generated from template - Version: 3.3.1
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.3.1
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    ruby ruby-bundler ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN useradd -m -u 65532 -s /usr/bin/false ruby 2>/dev/null || true
RUN mkdir -p /app /var/log/ruby /var/cache/ruby 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ruby ca-certificates 
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/ruby /var/log/ruby
COPY --from=builder --chown=65532:65532 /var/cache/ruby /var/cache/ruby
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["ruby"]
LABEL org.opencontainers.image.title="ruby" \
      org.opencontainers.image.version="3.3.1" \
      org.opencontainers.image.vendor="Ruby" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.hardened="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM