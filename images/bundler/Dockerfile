# =============================================================================
# EVERGREEN HARDENED BUNDLER
# Generated from template - Version: 2.5.0
# Constraint: debian-slim - Ruby runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.5.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ruby ruby-dev ca-certificates curl build-base || true && \
    gem install bundler -v 2.5.0 --no-document && \
    strip /usr/local/bin/bundle 2>/dev/null || true && \
    strip /usr/local/bin/bundler 2>/dev/null || true && \
    adduser -u 65532 -D app 2>/dev/null || true && \
    mkdir -p /app /var/log/ruby /var/cache/ruby && chown -R app:app /app /var/log/ruby /var/cache/ruby 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["bundle"]
LABEL org.opencontainers.image.title="bundler" \
      org.opencontainers.image.description="bundler container image" \
      org.opencontainers.image.version="2.5.0" \
      org.opencontainers.image.vendor="Ruby Bundler" \
      org.opencontainers.image.source="https://github.com/rubygems/rubygems" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
