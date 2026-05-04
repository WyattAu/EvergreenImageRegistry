ARG VERSION=latest

FROM fluent/fluent-bit:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION=3.2.4
RUN apk add --no-cache curl ca-certificates
COPY --from=upstream /fluent-bit/bin/fluent-bit /usr/local/bin/fluent-bit
RUN mkdir -p /app /var/log/fluent-bit /var/cache/fluent-bit

WORKDIR /app

EXPOSE 2020
EXPOSE 9101

LABEL org.opencontainers.image.title="fluent-bit" org.opencontainers.image.version="3.2.4" org.opencontainers.image.vendor="Fluent" evergreen.image.tier="1" evergreen.constraint.nonroot="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms"
      org.opencontainers.image.description="Fluent Bit - fast lightweight log processor and forwarder" \
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:2020/ || exit 1
ENTRYPOINT ["fluent-bit"]
