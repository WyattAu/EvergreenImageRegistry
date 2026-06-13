ARG VERSION=v0.4.10
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM public.ecr.aws/zinc/zincsearch:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/zinc /var/cache/zinc 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=upstream /go/bin/zincsearch /usr/local/bin/zincsearch
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/zinc /var/log/zinc
COPY --from=builder /var/cache/zinc /var/cache/zinc

WORKDIR /tmp

EXPOSE 4080
EXPOSE 9101

LABEL org.opencontainers.image.title="zinc" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Evergreen hardened ZincSearch - lightweight alternative to Elasticsearch" org.opencontainers.image.vendor="ZincSearch" evergreen.image.tier="1" evergreen.image.category="database" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" \
      org.opencontainers.image.source="https://github.com/zinclabs/zinc"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:4080"]

ENTRYPOINT ["/shim", "run"]
