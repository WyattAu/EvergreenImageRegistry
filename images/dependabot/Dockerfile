ARG VERSION=0.275.1
ARG BUILD_DATE

FROM ghcr.io/github/dependabot-updater-internal:latest AS upstream
RUN mkdir -p /app /usr/local/bin 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ruby ruby-irb ruby-rdoc ca-certificates \
        git curl gnupg gmp mpdecimal libffi \
        readline ncurses yaml zlib nodejs npm || true
RUN mkdir -p /usr/lib/ruby /usr/local/bundle /app /home/dependabot 2>/dev/null || true
COPY --from=upstream /home/dependabot /home/dependabot
COPY --from=upstream /usr/local/bundle /usr/local/bundle
COPY --from=upstream /usr/local/bin /usr/local/bin
COPY --from=upstream /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /bin/false dependabot 2>/dev/null || true && \
    chown -R 65532:65532 /app /usr/local/bundle /home/dependabot 2>/dev/null || true
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
