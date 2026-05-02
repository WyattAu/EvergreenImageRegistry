ARG VERSION=nightly

FROM getsentry/sentry:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates libpq libxml2 libxslt libffi openssl git
COPY --from=upstream /usr/src/sentry /opt/sentry
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/sentry 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 9000
ENTRYPOINT ["sentry"]
CMD ["web"]
LABEL org.opencontainers.image.title="sentry"       org.opencontainers.image.version="26.4.1"       org.opencontainers.image.vendor="Sentry"       org.opencontainers.image.source="https://github.com/getsentry/self-hosted"       sovereign.image.tier="2"       sovereign.image.category="monitoring"       sovereign.image.status="functional"       sovereign.constraint.nonroot="true"       sovereign.constraint.base="wolfi"       sovereign.hft.signal-handling="native"       sovereign.hft.shutdown-timeout="30s"       sovereign.hft.init-system="none"       sovereign.hft.startup-timeout="60000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
