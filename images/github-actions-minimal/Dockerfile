ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=2.334.0
ARG TARGETARCH
RUN mkdir -p /runner || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 --connect-timeout 30 --max-time 600 -fsSL "https://github.com/actions/runner/releases/download/v${VERSION}/actions-runner-linux-x64-${VERSION}.tar.gz" -o /runner.tar.gz 2>/dev/null ; \
    echo "ba46ba7ce3a4d7236b16fbe44419fb453bc08f866b24f04d549ec89f1722a29e  /runner.tar.gz" | sha256sum -c ; \
    mkdir -p /runner && if [ -f /runner.tar.gz ]; then tar -xzf /runner.tar.gz -C /runner 2>/dev/null ; rm -f /runner.tar.gz 2>/dev/null ; fi
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=2.334.0
RUN apk add --no-cache nodejs-20 npm ca-certificates git && \
    addgroup -S -g 10000 runner 2>/dev/null || true && adduser -u 65532 -G runner -D -h /app -s /bin/false runner 2>/dev/null || true && \
    mkdir -p /app /runner /home/runner/_work 2>/dev/null || true
COPY --from=builder /runner /app/runner
RUN chmod -R 755 /app/runner/bin 2>/dev/null || true && \
    chown -R 65532:65532 /app /runner /home/runner 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/app/runner/bin/Runner.Worker", "--", "--disableupdate"]
LABEL org.opencontainers.image.title="github-actions-minimal" \
      org.opencontainers.image.version="2.334.0" \
      org.opencontainers.image.vendor="GitHub" \
      org.opencontainers.image.source="https://github.com/actions/runner" \
      org.opencontainers.image.description="GitHub Actions Minimal Runner" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
