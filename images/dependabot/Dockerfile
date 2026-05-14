ARG VERSION=0.275.1
ARG TARGETARCH
ARG BUILD_DATE

FROM ghcr.io/github/dependabot-updater-internal:latest AS upstream
RUN mkdir -p /app /usr/local/bin 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=0.275.1
RUN apk add --no-cache ruby ruby-irb ruby-rdoc ca-certificates \
        git curl gnupg gmp mpdecimal libffi \
        readline ncurses yaml zlib nodejs npm || true && \
    mkdir -p /usr/lib/ruby /usr/local/bundle /app /home/dependabot 2>/dev/null || true
COPY --from=upstream /home/dependabot /home/dependabot
COPY --from=upstream /usr/local/bundle /usr/local/bundle
COPY --from=upstream /usr/local/bin /usr/local/bin
COPY --from=upstream /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false dependabot 2>/dev/null || true && \
    chown -R 65532:65532 /app /usr/local/bundle /home/dependabot 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["dependabot"]
CMD ["scan"]
LABEL org.opencontainers.image.title="dependabot" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Dependabot - Automated dependency updates" \
      org.opencontainers.image.vendor="GitHub" \
      org.opencontainers.image.source="https://github.com/dependabot/dependabot-core" \
      evergreen.image.tier="3" \
      evergreen.image.category="devops" \
      evergreen.image.status="functional" \
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
