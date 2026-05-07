ARG VERSION=1.24.0
ARG BUILD_DATE

FROM gcr.io/kaniko-project/executor@sha256:4e7a52dd1f14872430652bb3b027405b8dfd17c4538751c620ac005741ef9698 AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /app /kaniko /var/log/kaniko /var/cache/kaniko 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION
RUN mkdir -p /etc/ssl /kaniko /usr/local /var/cache /var/log 2>/dev/null || true
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app /app
COPY --from=builder /kaniko /kaniko
COPY --from=builder /var/log/kaniko /var/log/kaniko
COPY --from=builder /var/cache/kaniko /var/cache/kaniko
COPY --from=upstream /kaniko/executor /kaniko/executor
COPY --from=upstream /kaniko/.docker /kaniko/.docker
COPY --from=upstream /usr/local/bin /usr/local/bin
RUN apk add --no-cache ca-certificates && \
    ln -sf /kaniko/executor /usr/local/bin/kaniko && \
    adduser -u 65532 -D kaniko 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/kaniko/executor"]
CMD ["--help"]
LABEL org.opencontainers.image.title="kaniko" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Google" \
      org.opencontainers.image.source="https://github.com/GoogleContainerTools/kaniko" \
      org.opencontainers.image.description="Evergreen hardened kaniko - container image builder" \
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
