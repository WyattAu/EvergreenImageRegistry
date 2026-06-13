ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.4.18.2805
ARG TARGETARCH
RUN mkdir -p /app || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/Readarr/Readarr/releases/download/v${VERSION}/Readarr.develop.0.4.18.2805.linux-core-x64.tar.gz" -o /tmp/Readarr.tar.gz ; \
    echo "842ab11fac4f2e103e57badeaac1e2d44636b14dc727a1123098a2597adc5141  /tmp/Readarr.tar.gz" | sha256sum -c ; \
    mkdir -p /app && \
    if [ -f /tmp/Readarr.tar.gz ]; then tar -xzf /tmp/Readarr.tar.gz -C /app && rm -f /tmp/Readarr.tar.gz ; fi ; \
    chmod +x /app/Readarr 2>/dev/null

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates curl 2>/dev/null && \
    adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/readarr /var/cache/readarr && chown -R 65532:65532 /var/log/readarr /var/cache/readarr 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8787
EXPOSE 9101


LABEL org.opencontainers.image.description="readarr container image" \
      org.opencontainers.image.source="https://github.com/Readarr/Readarr" \
            org.opencontainers.image.version="0.4.18.2805"

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8787"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="readarr" \
evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="3"
