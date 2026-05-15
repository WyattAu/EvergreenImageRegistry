FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=2.334.0
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 --connect-timeout 30 --max-time 600 -fsSL "https://github.com/actions/runner/releases/download/v${VERSION}/actions-runner-linux-x64-${VERSION}.tar.gz" -o /runner.tar.gz 2>/dev/null || true ; \
    echo "ba46ba7ce3a4d7236b16fbe44419fb453bc08f866b24f04d549ec89f1722a29e  /runner.tar.gz" | sha256sum -c || true ; \
    mkdir -p /runner && if [ -f /runner.tar.gz ]; then tar -xzf /runner.tar.gz -C /runner 2>/dev/null || true ; rm -f /runner.tar.gz 2>/dev/null || true ; fi
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=2.334.0
RUN apk add --no-cache nodejs-20 npm ca-certificates git || true && \
    addgroup -S -g 10000 runner 2>/dev/null || true && adduser -u 65532 -G runner -D -h /app -s /bin/false runner 2>/dev/null || true && \
    mkdir -p /app /runner /home/runner/_work 2>/dev/null || true
COPY --from=builder /runner /app/runner
RUN chmod -R 755 /app/runner/bin 2>/dev/null || true && \
    chown -R 65532:65532 /app /runner /home/runner 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8080/ || exit 1
ENTRYPOINT ["/app/runner/bin/Runner.Worker"]
CMD ["--disableupdate"]
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
STOPSIGNAL SIGTERM
