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
    ruby ruby-bundler ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin ruby 2>/dev/null || true
RUN mkdir -p /app /var/log/ruby /var/cache/ruby

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ruby ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* && \
    apt-get purge -y --auto-remove apt apt-get dpkg 2>/dev/null || true
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /var/log/ruby /var/log/ruby
COPY --from=builder --chown=65534:65534 /var/cache/ruby /var/cache/ruby
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ruby --version
ENTRYPOINT ["ruby"]
LABEL org.opencontainers.image.title="ruby" \
      org.opencontainers.image.version="3.3.1" \
      org.opencontainers.image.vendor="Ruby" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.constraint.hardened="true"
