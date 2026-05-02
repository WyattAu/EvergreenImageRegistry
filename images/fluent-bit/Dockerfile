ARG VERSION=latest

FROM fluent/fluent-bit:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION=3.2.4
RUN apk add --no-cache curl ca-certificates
COPY --from=upstream /fluent-bit/bin/fluent-bit /usr/local/bin/fluent-bit
RUN mkdir -p /app /var/log/fluent-bit /var/cache/fluent-bit

WORKDIR /app

EXPOSE 2020
EXPOSE 9101

LABEL org.opencontainers.image.title="fluent-bit" org.opencontainers.image.version="3.2.4" org.opencontainers.image.vendor="Fluent" sovereign.image.tier="1" sovereign.constraint.nonroot="true" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["fluent-bit"]
