ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder
ARG VERSION=0.16.2
ARG TARGETARCH
RUN mkdir -p /usr/local/bin/stalwart || true
RUN apk add --no-cache wget ca-certificates && \
    wget -t 3 -T 10 -qO /tmp/stalwart.tar.gz "https://github.com/stalwartlabs/stalwart/releases/download/v${VERSION}/stalwart-x86_64-unknown-linux-musl.tar.gz" && \
    tar -xzf /tmp/stalwart.tar.gz -C /tmp && \
    mv /tmp/stalwart /usr/local/bin/stalwart && \
    chmod +x /usr/local/bin/stalwart && \
    strip /usr/local/bin/stalwart
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=0.16.2
RUN apk add --no-cache ca-certificates && \
    addgroup -S -g 10000 stalwart 2>/dev/null || true && \
    adduser -u 65532 -G stalwart -D -h /app -s /bin/false stalwart 2>/dev/null || true && \
    mkdir -p /app /var/lib/stalwart /etc/stalwart /var/log/stalwart 2>/dev/null || true
COPY --from=builder /usr/local/bin/stalwart /usr/local/bin/stalwart
RUN chown -R 65532:65532 /app /var/lib/stalwart /etc/stalwart /var/log/stalwart 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 25 143 465 587 993

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:25"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/usr/local/bin/stalwart", "--", "mail"]
LABEL org.opencontainers.image.title="stalwart-bitnami" \
      org.opencontainers.image.description="Stalwart Mail Server (Bitnami variant) - all-in-one mail server" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="stalwartlabs" \
      org.opencontainers.image.source="https://github.com/stalwartlabs/stalwart" \
      evergreen.image.tier="2" \
      evergreen.image.category="email" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="tcp"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
